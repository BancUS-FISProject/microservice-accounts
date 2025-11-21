import time

from quart import Quart, jsonify
from quart_schema import QuartSchema, Tag

from .core.config import settings
from .core import external_connections as ext

from logging import getLogger
from .utils.LoggerHandlers import get_file_handler, get_console_handler

from .api.v1.Accounts_blueprint import bp as accounts_bp_v1
from .api.v1.Health_blueprint import bp as health_bp_v1

## Logger configuration ##
logger = getLogger()
logger.setLevel(settings.LOG_LEVEL)
logger.addHandler(get_file_handler())
logger.addHandler(get_console_handler())
logger.propagate = False
## Logger configuration ##

def create_app():
    
    app = Quart("microservice-accounts",)
    
    settings.HEALTH_STATUS = 0
    
    # Load settings
    app.config.from_object(settings)
    logger.info("Settings loaded.")
    
    # Load health.
    app.register_blueprint(health_bp_v1)
    logger.info("Health route registered")
    
    # Open API Specification
    schema = QuartSchema()
    schema.tags = [
        Tag(name="v1", description="API version 1"),
    ]
    schema.openapi_path = "/api/openapi.json"
    schema.swagger_ui_path = "/api/docs"
    schema.init_app(app)
    # Open API Specification
    
    # Set up everything before serving the service
    async def initialize_resources():
        
        logger.info("Service is starting up...")
        
        # Database
        await connect_database()
        settings.REDIS_AVAILABLE = await connect_redis()
        
        if settings.REDIS_AVAILABLE:
            logger.info("Service started successfully")
        else:
            logger.info("Service started. Redis connection failed. Only local cache available.")
        settings.HEALTH_STATUS = 1
        # Load routes
        app.register_blueprint(accounts_bp_v1)
        logger.info("All routes registered")
    
    @app.before_serving
    async def startup():
        app.add_background_task(initialize_resources)
        app.add_background_task(ext.start_connection_monitor)
    
    # Release all resources before shutting down
    @app.after_serving
    async def shutdown():
        logger.info("Service is shutting down...")
        
        ext.close_db_client()
        
        logger.info("Service shut down complete.")
    
    return app

async def connect_database():
    i = 3
    success = False
    while i > 0 and not success:
        try:
            logger.info("Awaiting database connection...")
            await ext.init_db_client()
            logger.info("Database connection initialized.")
            success = True
        except Exception as e:
            logger.error("Database connection failed")
            logger.debug(e)
        finally:
            i = i - 1
            if i != 0 and not success:
                time.sleep(3)
                logger.info("Retrying database connection")
    if not success:
        logger.error(f"Database connection failed after 3 tries")
        raise Exception("Database connection failed")

async def connect_redis():
    i = 3
    success = False
    while i > 0 and not success:
        try:
            logger.info("Awaiting redis connection...")
            await ext.init_redis_client()
            logger.info("Redis connection initialized.")
            success = True
        except Exception as e:
            logger.error("Redis connection failed")
            logger.debug(e)
        finally:
            i = i - 1
            if i != 0 and not success:
                time.sleep(3)
                logger.info("Retrying redis connection")
    
    if not success:
        logger.error(f"Redis connection failed after 3 tries")
        
    return success