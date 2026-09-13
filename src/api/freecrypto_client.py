import requests
from src.config.settings import API_KEY, BASE_URL, REQUEST_TIMEOUT
from src.utils.logger import get_logger

logger = get_logger(__name__)

class FreeCryptoClient:
    def __init__(self):
        if not API_KEY:
            raise ValueError("Free API Key not set. Check your .env file.")

        self.base_url = f"{BASE_URL}/v1"
        self.headers = {
            "Authorization" : f"Bearer {API_KEY}"
        }

    def _get(self, endpoint: str, params: dict = None) -> dict:
        """
        Internal method that makes all GET requests.
        Every public method calls this — so error handling lives in one place.
        """
        url = f"{self.base_url}/{endpoint}"
        logger.debug(f"GET{url} | params: {params}")

        try: 
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status() # raises HTTPError for 4xx/5xx responses
            return response.json()
        
        except requests.exceptions.Timeout:
            logger.error(f"Request timed out: {url}")
            raise

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error {response.status_code} for {url}: {e}")
            raise

        except requests.exceptions.ConnectionError:
            logger.error(f"Connection Failed: {url}")
            raise

        except requests.exceptions.RequestException as e:
            logger.error(f"Unexpected request error for {url}: {e}")
            raise

    def get_data(self, symbols: list[str])-> list[dict]:
        """
        GET /getData
        Fetches live market data for one or more symbols.
        symbols: e.g. ["BTC", "ETH", "SOL"]
        """
        results = []
        for symbol in symbols:
            response = self._get("getData", params={"symbol": symbol})
            items = response.get("symbols", [])
            if items:
                results.extend(items)
            else:
                logger.warning(f"No data returned for symbol: {symbol}")
        if not results:
            raise ValueError("getData returned no data for any symbol — possible invalid API key")
        return results


    def get_crypto_list(self) -> list[dict]:
        """
        GET /getCryptoList
        Returns the full list of supported crypto symbols.
        Response shape: { "status": true, "resultset_size": N, "result": [...] }
        """
        response = self._get("getCryptoList")
        return response.get("result", [])

    def get_exchange(self, exchange: str) -> list[dict]:
        """
        GET /getExchange
        Returns all trading pairs for a given exchange.
        Response shape: { "status": "success", "symbols": [...] }
        exchange: e.g. "binance"
        """
        response = self._get("getExchange", params={"exchange": exchange})
        return response.get("symbols",[])

    def get_conversion(self, from_symbol: str, to_symbol: str, amount: float = 1.0) -> dict:
        """
        GET /getConversion
        Converts an amount from one symbol to another.
        e.g. from_symbol="BTC", to_symbol="USD", amount=20
        """
        params = {
            "from" : from_symbol,
            "to" : to_symbol,
            "amount" : amount
        }
        return self._get("getConversion", params=params)
    


        

