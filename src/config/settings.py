import os
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("FREECRYPTO_API_KEY")

BASE_URL = "https://api.freecryptoapi.com"
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")

# Fail fast at startup if api key is missing
if not API_KEY:
    raise ValueError("Free API KEY is not set. Add it to you .env file.")

# Request setting
REQUEST_TIMEOUT = 30

# Set to "local" to save files locally, or "blob" to save to Azure
STORAGE_TYPE = "blob"

ENDPOINTS = {
    "get_data":      "/getData",
    "get_top":       "/getTop",
    "get_crypto_list": "/getCryptoList",
    "get_exchange":  "/getExchange",
    "get_conversion": "/getConversion",
}

CRYPTOCURRENCIES = [
    "BTC", "ETH", "USDT", "BNB", "USDC",
    "XRP", "SOL", "TRX", "STETH", "HYPE",
    "DOGE", "USDS", "LEO", "ADA", "LTC",
]

# all directional pairs e.g. BTC->ETH and ETH->BTC are separate
CONVERSION_PAIRS = [
    (a, b) for a in CRYPTOCURRENCIES for b in CRYPTOCURRENCIES if a != b
]