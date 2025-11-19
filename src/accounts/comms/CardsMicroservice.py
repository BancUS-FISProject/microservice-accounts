from logging import getLogger

import httpx

from ..core.config import settings
from ..models.Cards import CreateCardRequest, CreateCardResponse
from ..models.Empty import EmptyError503

logger = getLogger()
logger.setLevel(settings.LOG_LEVEL)

async def create_card(card_data: CreateCardRequest) -> CreateCardResponse | EmptyError503:
    # Todo conn management when card microservice is available
    async with httpx.AsyncClient() as client:
        try:
            payload = card_data.model_dump(by_alias=True)
            
            response = await client.post(
                f"{settings.CARD_MICROSERVICE_BASE_URL}{settings.CARD_MICROSERVICE_CREATE_CARD_ENDPOINT}",
                json=payload,
                timeout=10.0
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            return CreateCardResponse(**response_data)
        
        except httpx.HTTPStatusError as e:
            logger.info("Card microservice is not responding")
            logger.error(e)
            return EmptyError503()
        except Exception as e:
            logger.info("Card microservice is not responding")
            logger.error(e)
            return EmptyError503()