from datetime import datetime

from quart import Blueprint
from quart_schema import validate_request, validate_response, tag

from ...models.Accounts import AccountCreate, AccountUpdate, AccountView, AccountUpdateFunds, AccountBase

from ...services.Accounts_service import AccountService

from logging import getLogger
from ...core.config import settings

logger = getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)

bp = Blueprint("accounts_v1", __name__, url_prefix="/v1/accounts")


@bp.post("/")
@validate_request(AccountCreate)
@validate_response(AccountView)
@tag(["v1"])
async def create_account(data: AccountCreate):
    service = AccountService()
    return await service.create_new_account(data)

@bp.get("/<string:iban>")
@validate_response(AccountView)
@tag(["v1"])
async def view_account(iban: str):
    service = AccountService()
    return await service.get_account_by_iban(iban)

@bp.patch("/<int:iban>")
@validate_request(AccountUpdate)
@validate_response(AccountView)
@tag(["v1"])
async def update_account(iban: int):
    pass

@bp.patch("/operation/<int:iban>")
@validate_request(AccountUpdateFunds)
@validate_response(AccountView)
@tag(["v1"])
async def update_account_funds(iban: int):
    pass

@bp.delete("/<int:iban>")
@tag(["v1"])
async def delete_account(iban: int):
    pass

@bp.patch("/<int:iban>/block")
@validate_response(AccountView)
@tag(["v1"])
async def block_account(iban: int):
    pass

@bp.patch("/<int:iban>/unblock")
@validate_response(AccountView)
@tag(["v1"])
async def unblock_account(iban: int):
    pass