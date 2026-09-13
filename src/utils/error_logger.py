import json
from datetime import datetime, timezone
from azure.storage.blob import BlobServiceClient
from src.config.settings import AZURE_STORAGE_CONNECTION_STRING, AZURE_CONTAINER_NAME
from src.utils.logger import get_logger

logger = get_logger(__name__)


def log_error_to_blob(endpoint: str, error: Exception, context: str = "") -> None:
    now = datetime.now(timezone.utc)

    blob_path = (
        f"error_logs/"
        f"year={now.strftime('%Y')}/"
        f"month={now.strftime('%m')}/"
        f"day={now.strftime('%d')}/"
        f"error_{endpoint}_{now.strftime('%Y%m%d_%H%M%S%f')}.json"
    )

    payload = {
        "timestamp": now.isoformat(),
        "endpoint": endpoint,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context,
    }

    try:
        content = json.dumps(payload, indent=2).encode("utf-8")
        client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        blob_client = client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=blob_path)
        blob_client.upload_blob(content, overwrite=True)
        logger.info(f"Error log written to blob: {blob_path}")
    except Exception as e:
        # fallback — if blob write fails, at least log locally
        logger.error(f"Failed to write error log to blob: {e}")