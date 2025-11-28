from logging import getLogger

import httpx

from ..core.config import settings
from ..models.Cards import CreateCardRequest, CreateCardResponse, DeleteCardRequest, DeleteCardResponse

logger = getLogger()
logger.setLevel(settings.LOG_LEVEL)

async def create_card_call(card_data: CreateCardRequest) -> CreateCardResponse:
    async with httpx.AsyncClient() as client:
        payload = card_data.model_dump(by_alias=True)
        
        response = await client.post(
            f"{settings.CARD_MICROSERVICE_BASE_URL}{settings.CARD_MICROSERVICE_CREATE_CARD_ENDPOINT}",
            json=payload,
            timeout=10.0
        )
        
        response.raise_for_status()
        response_data = response.json()
        
        return CreateCardResponse(**response_data)
    
async def delete_card_call(card_data: DeleteCardRequest) -> DeleteCardResponse:
    async with httpx.AsyncClient() as client:
        payload = card_data.model_dump(by_alias=True)
        
        response = await client.post(
            f"{settings.CARD_MICROSERVICE_BASE_URL}{settings.CARD_MICROSERVICE_CREATE_CARD_ENDPOINT}",
            json=payload,
            timeout=10.0
            )
        
        response.raise_for_status()
        response_data = response.json()
        
        return DeleteCardResponse(**response_data)