from dataclasses import dataclass, field
from typing import Optional

@dataclass
class CryptoData:
    symbol: str
    price: float
    change_24h: float
    lowest: float
    highest: float
    date: str
    source_exchange: str
    market_cap: float = 0.0  # not provided by /getData
    volume: float = 0.0      # not provided by /getData


@dataclass
class CryptoListItem:
    """Represents a single entry from /getCryptoList"""
    id: str
    symbol: str
    source: str
    name: Optional[str] = None
    ohlc_available_from : Optional[str] = None
    history_available_from : Optional[str] = None

@dataclass
class ExchangePair:
    """Represents a single trading pair from /getExchage"""
    symbol: str
    last: float
    daily_change_percentage: float
    date: str

@dataclass
class ConversionResult:
    """Represents the responce from the /getConversion"""
    from_symbol: str
    to_symbol: str
    amount: float
    converted_amount: float
    rate: float