from src.api.freecrypto_client import FreeCryptoClient
from src.config.settings import CRYPTOCURRENCIES, CONVERSION_PAIRS
from src.models.crypto import CryptoData, CryptoListItem, ExchangePair, ConversionResult
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CryptoService:

    def __init__(self):
        self.client = FreeCryptoClient()

    def get_market_data(self) -> list[CryptoData]:
        logger.info(f"Fetching market data for: {CRYPTOCURRENCIES}")
        raw = self.client.get_data(CRYPTOCURRENCIES)

        results = []
        for item in raw:
            try:
                results.append(CryptoData(
                    symbol=item["symbol"],
                    price=float(item["last"]),
                    change_24h=float(item["daily_change_percentage"]),
                    lowest=float(item["lowest"]),
                    highest=float(item["highest"]),
                    date=item["date"],
                    source_exchange=item["source_exchange"],
                ))
            except (KeyError, ValueError) as e:
                logger.warning(f"Skipping malformed getData entry: {e} | raw: {item}")

        if not results:
            raise ValueError("get_market_data returned no valid records — possible invalid API key or empty response")
        return results

    def get_crypto_list(self) -> list[CryptoListItem]:
        logger.info("Fetching crypto list")
        raw = self.client.get_crypto_list()

        results = []
        for item in raw:
            try:
                results.append(CryptoListItem(
                    id=item["id"],
                    symbol=item["symbol"],
                    source=item["source"],
                    name=item.get("name") or None,
                    ohlc_available_from=item.get("ohlc_available_from"),
                    history_available_from=item.get("history_available_from"),
                ))
            except KeyError as e:
                logger.warning(f"Skipping malformed getCryptoList entry: {e}")

        if not results:
            raise ValueError("get_crypto_list returned no valid records — possible invalid API key or empty response")
        return results

    def get_exchange_data(self, exchange: str) -> list[ExchangePair]:
        logger.info(f"Fetching exchange data for: {exchange}")
        raw = self.client.get_exchange(exchange)

        results = []
        for item in raw:
            try:
                results.append(ExchangePair(
                    symbol=item["symbol"],
                    last=float(item["last"]),
                    daily_change_percentage=float(item["daily_change_percentage"]),
                    date=item["date"],
                ))
            except (KeyError, ValueError) as e:
                logger.warning(f"Skipping malformed getExchange entry: {e}")

        if not results:
            raise ValueError(f"get_exchange_data returned no valid records for exchange: {exchange}")
        return results

    def get_all_conversions(self, amount: float = 1.0) -> list[ConversionResult]:
        """Fetch all cross-conversions between CRYPTOCURRENCIES — one API call per pair."""
        logger.info(f"Fetching {len(CONVERSION_PAIRS)} conversion pairs")
        results = []
        for from_symbol, to_symbol in CONVERSION_PAIRS:
            try:
                result = self.get_conversion(from_symbol, to_symbol, amount)
                results.append(result)
            except ValueError as e:
                logger.warning(f"Skipping conversion {from_symbol}->{to_symbol}: {e}")
        if not results:
            raise ValueError("get_all_conversions returned no valid results")
        return results

    def get_conversion(self, from_symbol: str, to_symbol: str, amount: float = 1.0) -> ConversionResult:
        logger.info(f"Converting {amount} {from_symbol} -> {to_symbol}")
        raw = self.client.get_conversion(from_symbol, to_symbol, amount)

        try:
            converted = float(raw["result"])
            return ConversionResult(
                from_symbol=from_symbol,
                to_symbol=to_symbol,
                amount=amount,
                converted_amount=converted,
                rate=converted / amount,
            )
        except (KeyError, ValueError) as e:
            error_msg = raw.get("error", str(e))
            logger.error(f"Failed to parse conversion response: {e} | raw: {raw}")
            raise ValueError(f"Conversion API error: {error_msg}")