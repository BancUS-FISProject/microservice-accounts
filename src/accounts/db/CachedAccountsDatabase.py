from typing import Optional, Dict
from logging import getLogger

from ..models.Accounts import (
    AccountUpdate, AccountView,
    AccountUpdatebalance
    )
from ..models.Cards import CreateCardResponse
from .AccountsDatabase import AccountRepository


logger = getLogger()


class CachedAccountRepository(AccountRepository):
    _cache: Dict[str, AccountView] = {}
    
    def __init__(self, db):
        super().__init__(db)
        
    
    async def find_account_by_iban(self, iban: str) -> AccountView | None:
        if iban in self._cache:
            logger.info(f"Cache HIT: account = {iban}")
            return self._cache[iban]
        
        account = await super().find_account_by_iban(iban)
        
        if account:
            self._cache[iban] = account
            logger.info(f"Cache MISS: account cached: iban = {iban}")
        
        return account
    
    async def delete_account_by_iban(self, iban: str) -> bool:
        result = await super().delete_account_by_iban(iban)
        
        if result and iban in self._cache:
            del self._cache[iban]
            logger.info(f"Cache invalidated (delete) for account: iban = {iban}")
        
        return result
    
    async def update_account_balance(self, iban: str, data: AccountUpdatebalance) -> AccountView | None:
        result = await super().update_account_balance(iban, data)
        self._invalidate_cache(iban)
        return result
    
    async def update_account(self, iban: str, data: AccountUpdate) -> AccountView | None:
        result = await super().update_account(iban, data)
        self._invalidate_cache(iban)
        return result
    
    async def block_account_by_iban(self, iban: str) -> AccountView | None:
        result = await super().block_account_by_iban(iban)
        self._invalidate_cache(iban)
        return result
    
    async def unblock_account_by_iban(self, iban: str) -> AccountView | None:
        result = await super().unblock_account_by_iban(iban)
        self._invalidate_cache(iban)
        return result
    
    async def account_add_card(self, iban: str, card: CreateCardResponse) -> AccountView | None:
        result = await super().account_add_card(iban, card)
        self._invalidate_cache(iban)
        return result
    
    def _invalidate_cache(self, iban: str):
        if iban in self._cache:
            del self._cache[iban]
            logger.info(f"Cache invalidated (update) for account: iban = {iban}")