# Generated Docker Image

With this command you can pull latest stable version of the microservice.

```commandline
docker pull alvvigsua/microservice-accounts:latest
```

Also, you can pull images from previous pull requests using the merge sha.

```commandline
docker pull alvvigsua/microservice-accounts:<tag>
```

```commandline
https://github.com/BancUS-FISProject/microservice-accounts/tree/<tag>
```

# Settings

```
MONGO_CONNECTION_STRING: str = "mongodb+srv://alvvigsua_db_user:8lwRGxRQlvETL3Ui@microservicio-cuentas.x2dz0fd.mongodb.net/?appName=Microservicio-Cuentas"
MONGO_DATABASE_NAME: str = "accounts"

LOG_LEVEL: str = "INFO"
LOG_FILE: str = "microservice-accounts.log"
LOG_BACKUP_COUNT: int = 7

REDIS_HOST: str = "localhost"
REDIS_PORT: int = 6379

CARD_MICROSERVICE_BASE_URL: str = "http://localhost:9000"
CARD_MICROSERVICE_CREATE_CARD_ENDPOINT: str = "/v1/card"
CARD_BREAKER_FAILS: int = 3
CARD_BREAKER_TIMEOUT: int = 30

CURRENCIES_MICROSERVICE_BASE_URL: str = "http://localhost:8010"
CURRENCIES_MICROSERVICE_EXCHANGE_ENDPOINT: str = "/v1/currency/convert"
CURRENCIES_BREAKER_FAILS: int = 3
CURRENCIES_BREAKER_TIMEOUT: int = 30
```