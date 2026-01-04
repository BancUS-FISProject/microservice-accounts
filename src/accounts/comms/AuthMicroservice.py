from logging import getLogger

import httpx

from ..core.config import settings
from ..models.Auth import *


logger = getLogger()
logger.setLevel(settings.LOG_LEVEL)


async def create_user_call(user_auth_create: CreaterAuthUser) -> None:
    async with httpx.AsyncClient() as client:
        payload = user_auth_create.model_dump(by_alias=True)
        
        response = await client.post(
            f"{settings.AUTH_MICROSERVICE_BASE_URL}{settings.AUTH_MICROSERVICE_CREATE_USER_ENDPOINT}",
            json=payload,
            timeout=10.0
            )
        
        response.raise_for_status()