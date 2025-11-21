import time

from quart import Quart, jsonify
from quart_schema import QuartSchema, Tag

from .core.config import settings
from .core import external_connections as ext

from logging import getLogger
from .utils.LoggerHandlers import get_file_handler, get_console_handler

from .api.v1.Accounts_blueprint import bp as accounts_bp_v1

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
    
    # Load blueprints.
    app.register_blueprint(accounts_bp_v1)
    logger.info("Routes registered")
    
    @app.route("/health")
    async def health_check():
        if settings.HEALTH_STATUS == 1:
            return jsonify({"status": "UP", "service": "accounts"}), 200
        else:
            return jsonify({"status": "STARTING", "detail": "Connecting to resources..."}), 503
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
        i = 5
        success = False
        while i > 0 and not success:
            try:
                logger.info("Awaiting database connection...")
                await ext.init_db_client()
                logger.info("Database connection initialized.")
                success = True
            except Exception as e:
                logger.error("Database connection failed...")
                logger.debug(e)
            finally:
                i = i - 1
                if i != 0 and not success:
                    time.sleep(3)
                    logger.info("Retrying database connection...")
        if not success:
            logger.error(f"Database connection failed after {i} tries")
            raise Exception("Database connection failed")
        
        i = 5
        success = False
        while i > 0 and not success:
            try:
                logger.info("Awaiting redis connection...")
                await ext.init_redis_client()
                logger.info("Redis connection initialized.")
                success = True
            except Exception as e:
                logger.error("Redis connection failed...")
                logger.debug(e)
            finally:
                i = i - 1
                if i != 0 and not success:
                    time.sleep(3)
                    logger.info("Retrying redis connection...")
                
        if not success:
            logger.error(f"Redis connection failed after {i} tries")
            raise Exception("Redis connection failed")
        
        logger.info("Service started successfully")
        settings.HEALTH_STATUS = 1
    
    @app.before_serving
    async def startup():
        app.add_background_task(initialize_resources)
    
    # Release all resources before shutting down
    @app.after_serving
    async def shutdown():
        logger.info("Service is shutting down...")
        
        ext.close_db_client()
        
        logger.info("Service shut down complete.")
    
    return app