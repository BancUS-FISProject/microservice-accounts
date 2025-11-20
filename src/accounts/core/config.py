from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    # database config
    MONGO_CONNECTION_STRING: str = "mongodb://bankus_user:bankus_secret_pass@localhost:27017"
    MONGO_DATABASE_NAME: str = "accounts"
    
    # Log config
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "log.txt"
    LOG_BACKUP_COUNT: int = 7
    
    #Redis Config
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # Cards microservice config
    CARD_MICROSERVICE_BASE_URL: str = "http://localhost:9000"
    CARD_MICROSERVICE_CREATE_CARD_ENDPOINT: str = "/v1/card"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

settings = Settings()