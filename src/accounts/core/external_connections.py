import asyncio
import sys

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from redis.asyncio import Redis

from .config import settings

from logging import getLogger

logger = getLogger()
logger.setLevel(settings.LOG_LEVEL)

db_client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None

redis: Redis | None = None

first_wait = True

async def init_redis_client():
    global redis
    redis = await Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)
    await redis.ping()
    


async def init_db_client():
    global db_client, db
    logger.info(f"Connecting to Database.")
    try:
        db_client = AsyncIOMotorClient(
            settings.MONGO_CONNECTION_STRING,
            maxPoolSize=100,
            minPoolSize=10,
            timeoutMS=5000
            )
        await db_client.admin.command('ping')
        
        db = db_client[settings.MONGO_DATABASE_NAME]
    
    except Exception as e:
        logger.error("Error connecting to database")
        logger.debug(e)
        raise e
    logger.info("Database connected")
    
    
    logger.info("Checking collections...")
    required_collections = ["accounts"]
    
    try:
        existing_collections = await db.list_collection_names()
        
        for collection_name in required_collections:
            if collection_name not in existing_collections:
                await db.create_collection(collection_name)
                logger.info(f"Collection '{collection_name}' created.")
            else:
                logger.info(f"Collection '{collection_name}' already exists.")
    
    except Exception as e:
        logger.error(f"Error checking/creating collections: {e}")
        raise
        
    logger.info("Database client initialized and collections checked.")
    
def close_db_client():
    global db_client, db
    logger.info(f"Closing Database")
    try:
        db_client.close()
    except Exception as e:
        logger.error("Error closing database")
        logger.debug(e)

async def start_connection_monitor(check_interval_seconds=10):
    global first_wait
    if first_wait:
        await asyncio.sleep(check_interval_seconds)
        first_wait = False
        
    logger.info("Starting background connection monitor...")
    
    while True:
        # Redis check
        try:
            if redis is None:
                await init_redis_client()
            else:
                await redis.ping()
            settings.REDIS_AVAILABLE = True
        except Exception as e:
            settings.REDIS_AVAILABLE = False
            logger.error(f"Watchdog: Redis connection lost. Attempting to reconnect...")
            logger.debug(e)
            try:
                await init_redis_client()
                logger.warning("Watchdog: Redis reconnected successfully.")
                settings.REDIS_AVAILABLE = True
            except Exception as e:
                logger.warning("Watchdog: Redis reconnection failed. Will try again in next cycle.")
                logger.debug(e)
        
        # Database check
        try:
            if db_client is None:
                await init_db_client()
            else:
                await db_client.admin.command('ping')
        except Exception as e:
            logger.critical(f"Watchdog: Database connection lost. Attempting CRITICAL reconnection...")
            logger.debug(e)
            
            try:
                await init_db_client()
                logger.info("Watchdog: Database reconnected successfully.")
            except Exception as fatal_error:
                logger.critical(f"Watchdog: FATAL - Could not reconnect to DB. Exiting application.")
                logger.debug(fatal_error)
                close_db_client()
                sys.exit(1)
                
        await asyncio.sleep(check_interval_seconds)