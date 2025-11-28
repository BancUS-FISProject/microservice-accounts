from datetime import timedelta
from logging import getLogger
import httpx
from aiobreaker import CircuitBreaker, CircuitBreakerError

from ..core.config import settings
from ..comms.CardsMicroservice import create_card_call, delete_card_call
from ..models.Cards import CreateCardRequest, CreateCardResponse, DeleteCardRequest, DeleteCardResponse
from ..models.Empty import EmptyError503

logger = getLogger()

cards_breaker = CircuitBreaker(
    fail_max=settings.CARD_BREAKER_FAILS,
    timeout_duration=timedelta(seconds=settings.CARD_BREAKER_TIMEOUT)
)

async def create_card(card_data: CreateCardRequest) -> CreateCardResponse | EmptyError503:
    try:
        return await cards_breaker.call_async(create_card_call, card_data)

    except CircuitBreakerError:
        logger.warning(f"Circuit Breaker Open: Skipping creation for card")
        return EmptyError503()

    except httpx.HTTPStatusError as e:
        logger.error(f"Card Microservice returned error status: {e.response.status_code} - {e}")
        return EmptyError503()

    except (httpx.RequestError, TimeoutError) as e:
        logger.error(f"Card Microservice connection failed: {e}")
        return EmptyError503()

    except Exception as e:
        logger.exception(f"Unexpected error in create_card service: {e}")
        return EmptyError503()


async def delete_card(card_data: DeleteCardRequest) -> DeleteCardResponse | EmptyError503:
    try:
        return await cards_breaker.call_async(delete_card_call, card_data)

    except CircuitBreakerError:
        logger.warning(f"Circuit Breaker Open: Skipping deletion for card")
        return EmptyError503()

    except httpx.HTTPStatusError as e:
        logger.error(f"Card Microservice returned error status: {e.response.status_code} - {e}")
        return EmptyError503()

    except (httpx.RequestError, TimeoutError) as e:
        logger.error(f"Card Microservice connection failed: {e}")
        return EmptyError503()

    except Exception as e:
        logger.exception(f"Unexpected error in delete_card service: {e}")
        return EmptyError503()