from logging import getLogger

from ..core.config import settings
from ..models.Accounts import AccountCreate, AccountUpdate, AccountView, AccountUpdatebalance, AccountBase
from ..models.Cards import CreateCardResponse, DeleteCardRequest, DeleteCardResponse


logger = getLogger()
logger.setLevel(settings.LOG_LEVEL)

class AccountRepository:
    
    def __init__(self, db):
        self.collection = db["accounts"]     # Collection used here
    
    async def insert_account(self, data: AccountBase) -> AccountView | None:
        account_doc = data.model_dump(by_alias=True)
        
        result = await self.collection.insert_one(account_doc)
        created_doc = await self.collection.find_one({"_id": result.inserted_id})
    
        if created_doc:
            res = AccountView.model_validate(created_doc)
            logger.info(f"Database operation: account created = {res.iban}")
            return res
        else:
            return None
    
    async def find_account_by_iban(self, iban: str) -> AccountView | None:
        doc = await self.collection.find_one({"iban": iban})
        if doc:
            res = AccountView.model_validate(doc)
            logger.info(f"Database operation: account found = {res.iban}")
            return res
        else:
            return None
    
    async def delete_account_by_iban(self, iban: str) -> bool:
        result = await self.collection.delete_one({"iban": iban})
        
        logger.info(f"Database operation: account deleted = {iban}")
        return result.deleted_count > 0
    
    async def update_account_balance(self, iban: str, data: AccountUpdatebalance) -> AccountView | None:
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        
        if not update_data:
            modified = await self.find_account_by_iban(iban)
            return AccountView.model_validate(modified)
        
        await self.collection.update_one(
            {"iban": iban},
            {"$set": update_data}
            )
        
        modified = await self.find_account_by_iban(iban)
        
        if modified:
            res = AccountView.model_validate(modified)
            logger.info(f"Database operation: account balance updated = {res.iban}")
            return res
        else:
            return None
    
    async def update_account(self, iban: str, data: AccountUpdate) -> AccountView | None:
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        
        if not update_data:
            modified = await self.find_account_by_iban(iban)
            return AccountView.model_validate(modified)
        
        await self.collection.update_one(
            {"iban": iban},
            {"$set": update_data}
            )
        
        modified = await self.find_account_by_iban(iban)
        
        if modified:
            res = AccountView.model_validate(modified)
            logger.info(f"Database operation: account updated = {res.iban}")
            return res
        else:
            return None
    
    async def block_account_by_iban(self, iban: str) -> AccountView | None:
        await self.collection.update_one(
            {"iban": iban},
            {"$set": {"isBlocked": True}}
            )
        
        modified = await self.find_account_by_iban(iban)
        
        if modified:
            res = AccountView.model_validate(modified)
            logger.info(f"Database operation: account blocked = {res.iban}")
            return res
        else:
            return None
    
    async def unblock_account_by_iban(self, iban: str) -> AccountView | None:
        await self.collection.update_one(
            {"iban": iban},
            {"$set": {"isBlocked": False}}
            )
        
        modified = await self.find_account_by_iban(iban)
        
        if modified:
            res = AccountView.model_validate(modified)
            logger.info(f"Database operation: account unblocked = {res.iban}")
            return res
        else:
            return None
    
    async def account_add_card(self, iban: str, card: CreateCardResponse) -> AccountView | None:
        await self.collection.update_one(
            {"iban": iban},
            {"$addToSet": {"cards": card.pan}}
        )
        
        modified = await self.find_account_by_iban(iban)
        if modified:
            res = AccountView.model_validate(modified)
            logger.info(f"Database operation: account cards updated = {res.iban}")
            return res
        else:
            return None
        
    async def account_delete_card(self, iban: str, card: DeleteCardResponse) -> bool:
        result = await self.collection.update_one(
            {"iban": iban},
            {"$pull": {"cards": card.pan}}
            )
    
        logger.info(f"Database operation: card {card.pan} deleted from account {iban}")
        return result.modified_count > 0