from quart import Blueprint, jsonify
from quart_schema import tag, document_response

from ...models.Health import Healthy, Starting


from logging import getLogger
from ...core.config import settings


logger = getLogger()
logger.setLevel(settings.LOG_LEVEL)

bp = Blueprint("health_v1", __name__, url_prefix="/v1")

@bp.route("/health")

@tag(['v1', 'health'])
@document_response(Starting, 503)
@document_response(Healthy, 200)
async def health_check():
    if settings.HEALTH_STATUS >= 1:
        return jsonify({"status": "UP", "service": "accounts"}), 200
    else:
        return jsonify({"status": "STARTING", "detail": "Connecting to resources..."}), 503