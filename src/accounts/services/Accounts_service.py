from ..core.config import settings
from ..db.RedisCachedAccountsDatabase import RedisCachedAccountRepository
from ..models.Accounts import AccountCreate, AccountUpdate, AccountView, AccountBase, AccountUpdatebalance
from ..db.AccountsDatabase import AccountRepository
from ..db.LocalCachedAccountsDatabase import LocalCachedAccountRepository
from ..core import external_connections as ext

from schwifty import IBAN

from ..models.AddtionalValidation import validate_iban, validate_email, validate_subscription
from ..models.Cards import CreateCardRequest, CreateCardResponse, DeleteCardRequest, DeleteCardResponse
from ..models.Empty import (EmptyPatch403, EmptyPatch404, EmptyPost404, EmptyError503, EmptyGet400,
                            EmptyPost400, EmptyPatch400, EmptyGet404, EmptyDelete400, EmptyDelete204, EmptyDelete404,
                            EmptyPatch204)

from ..models import AddtionalValidation as val

# Implement cache here

class AccountService:
    def __init__(self, repository: AccountRepository | None = None):
        if settings.REDIS_AVAILABLE:
            self.repo = repository or RedisCachedAccountRepository(ext.db, ext.redis)
        else:
            self.repo = repository or LocalCachedAccountRepository(ext.db)
    
    async def create_new_account(self, data: AccountCreate) -> AccountView | EmptyPost400:
        if not (val.validate_email(data.email) and val.validate_subscription(data.subscription)):
            return EmptyPost400()
        
        data_dict = data.model_dump(by_alias=True)
        
        iban_es = IBAN.random(country_code='ES')
        data_dict['iban'] = str(iban_es)
        
        new_account = AccountBase(**data_dict)
        
        return await self.repo.insert_account(new_account)
    
    async def get_account_by_iban(self, iban: str) -> AccountView | EmptyGet400 | EmptyGet404:
        if not validate_iban(iban):
            return EmptyGet400()
        res = await self.repo.find_account_by_iban(iban=iban)
        return res if res else EmptyGet404()
    
    async def account_update(self, iban:str, data: AccountUpdate) -> AccountView | EmptyPatch400 | EmptyPatch404:
        if data.email:
            if not validate_email(data.email):
                return EmptyPatch400()
        
        if data.subscription:
            if not validate_subscription(data.subscription):
                return EmptyPatch400()
        
        res = await self.repo.update_account(iban, data)
        return res if res else EmptyGet404()
    
    async def account_update_balance(self, iban:str, data: AccountUpdatebalance) -> (AccountView | EmptyPatch404 |
                                                                                     EmptyPatch403 | EmptyPatch400):
        if not validate_iban(iban):
            return EmptyPatch400()
        
        acc = await self.repo.find_account_by_iban(iban)
        if not acc:
            return EmptyPatch404()
        
        if acc.balance + data.balance >= 0 :
            data.balance = round(acc.balance + data.balance, 2)
            return await self.repo.update_account_balance(iban, data)
        else:
            return EmptyPatch403()
    
    async def delete_account(self, iban: str) -> EmptyDelete400 | EmptyDelete204 | EmptyDelete404:
        if not validate_iban(iban):
            return EmptyDelete400()
        
        res = await self.repo.delete_account_by_iban(iban)
        if res:
            return EmptyDelete204()
        else:
            return EmptyDelete404()
    
    async def block_account(self, iban: str) -> EmptyPatch204 | EmptyPatch400 | EmptyPatch404:
        if not validate_iban(iban):
            return EmptyPatch400()
        
        res = await self.repo.block_account_by_iban(iban)
        if res:
            return EmptyPatch204()
        else:
            return EmptyPatch404()
        
    
    async def unblock_account(self, iban: str) -> EmptyPatch204 | EmptyPatch400 | EmptyPatch404:
        if not validate_iban(iban):
            return EmptyPatch400()
        
        res = await self.repo.unblock_account_by_iban(iban)
        if res:
            return EmptyPatch204()
        else:
            return EmptyPatch404()

    async def account_create_card(self, iban: str) -> AccountView | EmptyPost400 | EmptyPost404 | EmptyError503:
        if not validate_iban(iban):
            return EmptyPost400()
        
        acc = await self.repo.find_account_by_iban(iban)
        if not acc:
            return EmptyPost404()
        
        # todo Mock data added while cards microservice is in development
        #res = create_card(CreateCardRequest(name=acc['name']))
        res = CreateCardResponse(pan="examplepan123123")
        
        if isinstance(res, CreateCardResponse):
             return await self.repo.account_add_card(iban, res)
        elif isinstance(res, EmptyError503):
            return EmptyError503()
        
        return await self.repo.find_account_by_iban(iban)
    
    async def account_delete_card(self, iban: str, data: DeleteCardRequest) -> (AccountView | EmptyPost400 | EmptyPost404 |
                                                                          EmptyError503):
        if not validate_iban(iban):
            return EmptyPost400()
        
        acc = await self.repo.find_account_by_iban(iban)
        if not acc:
            return EmptyPost404()
            
        # todo Mock data added while cards microservice is in development
        # res = delete_card(DeleteCardRequest(name=acc['name']))
        res = DeleteCardResponse(pan=data.pan)
        
        if isinstance(res, DeleteCardResponse):
            await self.repo.account_delete_card(iban, res)
        elif isinstance(res, EmptyError503):
            return EmptyError503()
        
        return await self.repo.find_account_by_iban(iban)
        
        