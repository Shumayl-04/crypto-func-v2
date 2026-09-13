from src.services.crypto_service import CryptoService
from src.storage.blob_storage import save_to_blob
from src.storage.local_storage import save_json
from src.config.settings import STORAGE_TYPE
from src.utils.error_logger import log_error_to_blob
from src.utils.retry import with_retry
from src.utils.logger import get_logger
from dataclasses import asdict

logger = get_logger(__name__)


def save(endpoint: str, data) -> None:
    if STORAGE_TYPE == "blob":
        save_to_blob(endpoint, data)
    else:
        save_json(endpoint, data)


def main():
    logger.info("Starting crypto ingestion run")
    service = CryptoService()

    try:
        def fetch_market_data():
            market_data = service.get_market_data()
            data = [asdict(coin) for coin in market_data]
            save("market_data", data)
        with_retry(fetch_market_data, endpoint="market_data")
    except Exception as e:
        logger.error(f"market_data failed: {e}")
        log_error_to_blob("market_data", e)

    try:
        def fetch_crypto_list():
            crypto_list = service.get_crypto_list()
            data = [asdict(item) for item in crypto_list]
            save("crypto_list", data)
        with_retry(fetch_crypto_list, endpoint="crypto_list")
    except Exception as e:
        logger.error(f"crypto_list failed: {e}")
        log_error_to_blob("crypto_list", e)

    try:
        def fetch_conversion():
            conversions = service.get_all_conversions(amount=1.0)
            data = [asdict(c) for c in conversions]
            save("conversions", data)
        with_retry(fetch_conversion, endpoint="conversions")
    except Exception as e:
        logger.error(f"conversions failed: {e}")
        log_error_to_blob("conversions", e)

    logger.info("Ingestion run complete")


if __name__ == "__main__":
    main()