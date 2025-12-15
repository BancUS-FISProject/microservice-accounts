from logging import getLogger
import redis.asyncio as redis

from ..models.Accounts import (
    AccountUpdate, AccountView,
    AccountUpdateBalance
    )
from ..models.Cards import CreateCardResponse, DeleteCardResponse, CardInfo
from .AccountsDatabase import AccountRepository

logger = getLogger()


class RedisCachedAccountRepository(AccountRepository):
    def __init__(self, db, redis_client: redis.Redis, ttl_seconds: int = 3600):
        super().__init__(db)
        self.redis = redis_client
        self.ttl = ttl_seconds
    
    def _get_key(self, iban: str) -> str:
        return f"account:{iban}"
    
    async def find_account_by_iban(self, iban: str) -> AccountView | None:
        key = self._get_key(iban)
        
        cached_data = await self.redis.get(key)
        
        if cached_data:
            try:
                logger.info(f"Cache HIT (Redis): account = {iban}")
                return AccountView.model_validate_json(cached_data)
            except Exception as e:
                logger.error(f"Error deserializing cache for {iban}: {e}")
        
        account = await super().find_account_by_iban(iban)
        
        if account:
            await self.redis.set(key, account.model_dump_json(), ex=self.ttl)
            logger.info(f"Cache MISS: account cached in Redis: iban = {iban}")
        
        return account
    
    async def delete_account_by_iban(self, iban: str) -> bool:
        result = await super().delete_account_by_iban(iban)
        
        if result:
            await self._invalidate_cache(iban)
            logger.info(f"Cache invalidated (delete) for account: iban = {iban}")
        
        return result
    
    async def update_account_balance(self, iban: str, data: AccountUpdateBalance) -> AccountView | None:
        await self._invalidate_cache(iban)
        result = await super().update_account_balance(iban, data)
        return result
    
    async def update_account(self, iban: str, data: AccountUpdate) -> AccountView | None:
        await self._invalidate_cache(iban)
        result = await super().update_account(iban, data)
        return result
    
    async def block_account_by_iban(self, iban: str) -> AccountView | None:
        await self._invalidate_cache(iban)
        result = await super().block_account_by_iban(iban)
        return result
    
    async def unblock_account_by_iban(self, iban: str) -> AccountView | None:
        await self._invalidate_cache(iban)
        result = await super().unblock_account_by_iban(iban)
        return result
    
    async def account_add_card(self, iban: str, card: CardInfo) -> AccountView | None:
        await self._invalidate_cache(iban)
        result = await super().account_add_card(iban, card)
        return result
    
    async def account_delete_card(self, iban: str, card: CardInfo) -> bool:
        result = await super().account_delete_card(iban, card)
        
        if result:
            await self._invalidate_cache(iban)
            logger.info(f"Cache invalidated (card delete) for account: iban = {iban}")
        
        return result
    
    async def _invalidate_cache(self, iban: str):
        key = self._get_key(iban)
        await self.redis.delete(key)
        logger.info(f"Cache key deleted: {key}")