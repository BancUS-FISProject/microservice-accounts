from logging import getLogger

import httpx

from ..core.config import settings
from ..models.Currencies import CurrenciesResponse

logger = getLogger()
logger.setLevel(settings.LOG_LEVEL)

async def exchange_currencies_call(from_currency: str, to_currency: str, original_amount: float) -> CurrenciesResponse:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=f"{settings.CURRENCIES_MICROSERVICE_BASE_URL}{settings.CURRENCIES_MICROSERVICE_EXCHANGE_ENDPOINT}",
            params={"from": from_currency, "to": to_currency, "amount": original_amount},
            )
        
        response.raise_for_status()
        response_data = response.json()
        return CurrenciesResponse(
            to_currency=response_data["to"],
            from_currency=response_data["from"],
            original_amount=response_data["original_amount"],
            converted_amount=response_data["converted_amount"]
        )