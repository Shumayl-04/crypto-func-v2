import os
import json
from datetime import datetime, timezone
from src.utils.logger import get_logger

logger = get_logger(__name__)

DATA_DIR = "data/local_storage"

def save_json(endpoint: str, data, source: str = "freecryptoapi") -> str:
    now = datetime.now(timezone.utc)

    folder = os.path.join(
        DATA_DIR,
        endpoint,
        f"year={now.strftime('%Y')}",
        f"month={now.strftime('%m')}",
        f"day={now.strftime('%d')}",
    )
    os.makedirs(folder, exist_ok=True)

    filename = f"{endpoint}_{now.strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(folder, filename)

    payload = {
        "ingestion_timestamp": now.isoformat(),
        "source": source,
        "endpoint": endpoint,
        "data": data,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=str)

    logger.info(f"Saved {endpoint} data to {filepath}")
    return filepath