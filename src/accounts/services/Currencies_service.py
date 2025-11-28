from datetime import timedelta
from logging import getLogger
import httpx
from aiobreaker import CircuitBreaker, CircuitBreakerError

from ..core.config import settings
from ..comms.CurrenciesMicroservice import exchange_currencies_call
from ..models.Currencies import CurrenciesResponse
from ..models.Empty import EmptyError503

logger = getLogger()

currencies_breaker = CircuitBreaker(
    fail_max=settings.CURRENCIES_BREAKER_FAILS,
    timeout_duration=timedelta(seconds=settings.CURRENCIES_BREAKER_TIMEOUT)
)

async def exchange_currencies(from_currency: str, to_currency: str, original_amount: float) -> CurrenciesResponse | EmptyError503:
    try:
        return await currencies_breaker.call_async(exchange_currencies_call, from_currency, to_currency, original_amount)

    except CircuitBreakerError:
        logger.warning(f"Circuit Breaker Open: Skipping exchange")
        return EmptyError503()

    except httpx.HTTPStatusError as e:
        logger.error(f"Currencies Microservice returned error status: {e.response.status_code} - {e}")
        return EmptyError503()

    except (httpx.RequestError, TimeoutError) as e:
        logger.error(f"Currencies Microservice connection failed: {e}")
        return EmptyError503()

    except Exception as e:
        logger.exception(f"Unexpected error in exchange_currencies service: {e}")
        return EmptyError503()