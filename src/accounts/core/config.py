from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Health config
    HEALTH_STATUS: int = 0
    HEALTH_STATUS_ROUTE: str = ""
    
    # database config
    MONGO_CONNECTION_STRING: str = "mongodb://bankus_user:bankus_secret_pass@localhost:27017"
    MONGO_DATABASE_NAME: str = "accounts"
    
    # Log config
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "microservice-accounts.log"
    LOG_BACKUP_COUNT: int = 7
    
    #Redis Config
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_AVAILABLE: bool = False
    
    # Cards microservice config
    CARD_MICROSERVICE_BASE_URL: str = "http://cards-microservice:8000"
    CARD_MICROSERVICE_CREATE_CARD_ENDPOINT: str = "/v1/cards"
    CARD_MICROSERVICE_DELETE_CARD_ENDPOINT: str = "/v1/cards/pan"  #ADD PAN at the end
    CARD_BREAKER_FAILS: int = 3
    CARD_BREAKER_TIMEOUT: int = 30
    
    # Currencies microservice config
    CURRENCIES_MICROSERVICE_BASE_URL: str = "http://currecies-microservice:8000"
    CURRENCIES_MICROSERVICE_EXCHANGE_ENDPOINT: str = "/v1/currency/convert"
    CURRENCIES_BREAKER_FAILS: int = 3
    CURRENCIES_BREAKER_TIMEOUT: int = 30
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

settings = Settings()