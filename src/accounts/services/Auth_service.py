from datetime import timedelta
from logging import getLogger
import httpx
from aiobreaker import CircuitBreaker, CircuitBreakerError

from ..comms.AuthMicroservice import create_user_call
from ..core.config import settings
from ..models.Auth import CreaterAuthUser
from ..models.Empty import EmptyError503

logger = getLogger()

auth_breaker = CircuitBreaker(
    fail_max=settings.AUTH_BREAKER_FAILS,
    timeout_duration=timedelta(seconds=settings.AUTH_BREAKER_TIMEOUT)
)

async def create_user(user_auth_create: CreaterAuthUser) -> bool | EmptyError503:
    try:
        await auth_breaker.call_async(create_user_call, user_auth_create)
        return True

    except CircuitBreakerError:
        logger.warning(f"Circuit Breaker Open: Skipping exchange")
        return EmptyError503()

    except httpx.HTTPStatusError as e:
        logger.error(f"Auth Microservice returned error status: {e.response.status_code} - {e}")
        return EmptyError503()

    except (httpx.RequestError, TimeoutError) as e:
        logger.error(f"Auth Microservice connection failed: {e}")
        return EmptyError503()

    except Exception as e:
        logger.exception(f"Unexpected error in create_user auth service: {e}")
        return EmptyError503()