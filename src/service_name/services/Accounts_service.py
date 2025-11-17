from ..models.Accounts import AccountCreate, AccountUpdate, AccountView, AccountBase
from ..db.AccountsRepository import AccountRepository
from ..core import extensions as ext

from schwifty import IBAN


class AccountService:
    def __init__(self, repository: AccountRepository | None = None):
        self.repo = repository or AccountRepository(ext.db)
    
    async def create_new_account(self, data: AccountCreate) -> AccountView:
        data_dict = data.model_dump(by_alias=True)
        
        iban_es = IBAN.random(country_code='ES')
        data_dict['iban'] = str(iban_es)
        
        new_account = AccountBase(**data_dict)
        
        return await self.repo.insert_account(new_account)
    
    async def get_account_by_iban(self, iban: str) -> AccountView | None:
        return await self.repo.find_account_by_iban(iban=iban)