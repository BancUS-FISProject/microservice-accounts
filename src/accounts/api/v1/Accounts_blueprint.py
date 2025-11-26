from quart import Blueprint, request, abort, jsonify
from quart_schema import validate_request, validate_response, tag, document_request, document_response, \
    ResponseSchemaValidationError

from ...models.Accounts import AccountCreate, AccountUpdate, AccountView, AccountUpdatebalance
from ...models.Cards import DeleteCardRequest
from ...models.Empty import EmptyGet404, EmptyPatch400, EmptyPatch403, EmptyPatch404, EmptyPost400, \
    EmptyPost404, EmptyError503, EmptyDelete204, EmptyGet400, EmptyDelete400, EmptyDelete404, EmptyDelete200, \
    EmptyPatch204

from ...services.Accounts_service import AccountService

from logging import getLogger
from ...core.config import settings

logger = getLogger()
logger.setLevel(settings.LOG_LEVEL)

bp = Blueprint("accounts_v1", __name__, url_prefix="/v1/accounts")

@bp.post("/")
@validate_request(AccountCreate)
@validate_response(AccountView, 201)
@document_response(EmptyPost400, 400)
@tag(["v1"])
async def create_account(data: AccountCreate):
    service = AccountService()
    res = await service.create_new_account(data)
    if isinstance(res, EmptyPost404):
        abort(400, description="Bad Request")
    return res, 201

@bp.get("/<string:iban>")
@validate_response(AccountView, 200)
@document_response(EmptyGet400, 400)
@document_response(EmptyGet404, 404)
@tag(["v1"])
async def view_account(iban: str):
    service = AccountService()
    res = await service.get_account_by_iban(iban)
    if isinstance(res, EmptyGet404):
        abort(404, description="Account not found")
    if isinstance(res, EmptyGet400):
        abort(400, description="Bad Request")
        
    return res

@bp.patch("/<string:iban>")
@document_request(AccountUpdate)    #Document request to allow patch individual fields
@validate_response(AccountView)
@document_response(EmptyPatch400, 400)
@document_response(EmptyPatch404, 404)
@tag(["v1"])
async def update_account(iban: str):
    service = AccountService()
    
    # Validate JSON here
    raw_data = await request.get_json()
    if raw_data is None:
        return abort(400, description="Bad Request")
    data = AccountUpdate(**raw_data)
    
    res = await service.account_update(iban, data)
    return res if res else abort(404, description="Account not found")

@bp.patch("/operation/<string:iban>")
@document_request(AccountUpdatebalance)
@validate_response(AccountView)
@document_response(EmptyPatch400, 400)
@document_response(EmptyPatch403, 403)
@document_response(EmptyPatch404, 404)
@tag(["v1"])
async def update_account_balance(iban: str):
    service = AccountService()
    
    # Validate JSON here
    raw_data = await request.get_json()
    if raw_data is None:
        return abort(400, description="Bad Request")
    data = AccountUpdatebalance(**raw_data)
    
    res = await service.account_update_balance(iban, data)
    if isinstance(res, EmptyPatch400):
        abort(400, description="Bad Request")
    if isinstance(res, EmptyPatch403):
        abort(403, description="Forbidden Operation - Not sufficient funds")
    elif isinstance(res, EmptyPatch404):
        abort(404, description="Account not found")
    return res

@bp.delete("/<string:iban>")
@document_response(EmptyDelete204, 204)
@document_response(EmptyDelete400, 400)
@document_response(EmptyDelete404, 404)
@tag(["v1"])
async def delete_account(iban: str):
    service = AccountService()
    res = await service.delete_account(iban)
    
    if isinstance(res, EmptyDelete400):
        abort(400, description="Bad Request")
    if isinstance(res, EmptyDelete404):
        abort(404, description="Account not found")
    return "",204

@bp.patch("/<string:iban>/block")
@validate_response(AccountView)
@document_response(EmptyPatch204, 204)
@document_response(EmptyPatch400, 400)
@document_response(EmptyPatch404, 404)
@tag(["v1"])
async def block_account(iban: str):
    service = AccountService()
    res = await service.block_account(iban)
    if isinstance(res, EmptyPatch400):
        abort(400, description="Bad Request")
    if isinstance(res, EmptyPatch404):
        abort(404, description="Account not found")
    return "", 204

@bp.patch("/<string:iban>/unblock")
@validate_response(AccountView)
@document_response(EmptyPatch204, 204)
@document_response(EmptyPatch400, 400)
@document_response(EmptyPatch404, 404)
@tag(["v1"])
async def unblock_account(iban: str):
    service = AccountService()
    res = await service.unblock_account(iban)
    if isinstance(res, EmptyPatch400):
        abort(400, description="Bad Request")
    if isinstance(res, EmptyPatch404):
        abort(404, description="Account not found")
    return "", 204

@bp.post("/card/<string:iban>")
@validate_response(AccountView, 200)
@document_response(EmptyPost400, 400)
@document_response(EmptyPost404, 404)
@document_response(EmptyError503, 503)
@tag(["v1"])
async def create_card_account(iban: str):
    # todo improve status code
    service = AccountService()
    res = await service.account_create_card(iban)
    if isinstance(res, EmptyPost400):
        abort(400, description="Bad Request")
    if isinstance(res, EmptyPost404):
        abort(404, description="Account not found")
    if isinstance(res, EmptyError503):
        abort(503, description="Microservice cards is unavailable")
    return res

@bp.delete("/card/<string:iban>")
@validate_request(DeleteCardRequest)
@document_response(EmptyDelete200, 200)
@document_response(EmptyPost400, 400)
@document_response(EmptyPost404, 404)
@document_response(EmptyError503, 503)
@tag(["v1"])
async def delete_card_account(iban: str, data: DeleteCardRequest):
    # todo improve status code
    service = AccountService()
    res = await service.account_delete_card(iban, data)
    if isinstance(res, EmptyPost400):
        abort(400, description="Bad Request")
    if isinstance(res, EmptyPost404):
        abort(404, description="Account not found")
    if isinstance(res, EmptyError503):
        abort(503, description="Microservice cards is unavailable")
    return res

@bp.errorhandler(ResponseSchemaValidationError)
async def handle_validation_error(error):
    return jsonify({
        "error": "Bad Request",
        "message": "Data input not valid",
        "details": error.validation_error.errors()
    }), 400
