import json
from datetime import datetime, timezone
from azure.storage.blob import BlobServiceClient
from src.config.settings import AZURE_STORAGE_CONNECTION_STRING, AZURE_CONTAINER_NAME
from src.utils.logger import get_logger

logger = get_logger(__name__)

def save_to_blob(endpoint: str, data, source: str = "freecryptoapi") -> str:
    """
    Writes API response data to ADLS Gen2 with the same structure as local storage.
    Path mirrors local: raw/{endpoint}/year=YYYY/month=MM/day=DD/filename.json
    """
    now = datetime.now(timezone.utc)

    blob_path = (
        f"landing/cryptoexchange_data/{endpoint}/"
        f"year={now.strftime('%Y')}/"
        f"month={now.strftime('%m')}/"
        f"day={now.strftime('%d')}/"
        f"{endpoint}_{now.strftime('%Y%m%d_%H%M%S')}.json"
    )

    payload = {
        "ingestion_timestamp": now.isoformat(),
        "source": source,
        "endpoint": endpoint,
        "data": data,
    }

    content = json.dumps(payload, indent=2, default=str).encode("utf-8")

    client =  BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    blob_client = client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=blob_path)
    blob_client.upload_blob(content, overwrite=True)

    logger.info(f"Upload {endpoint} to blob: {blob_path}")
    return blob_path