import math
import re
from typing import Dict, Any, Optional, Tuple
from src.client import BinanceClient
from src.logger import logger

class ValidationError(Exception):
    """Custom exception raised when order parameter validation fails."""
    pass

def round_to_step_size(value: float, step_size: float) -> float:
    """
    Rounds value down to the nearest multiple of step_size.
    Example: value=0.0126, step_size=0.001 -> 0.012
    """
    if step_size <= 0:
        return value
    precision = int(round(-math.log10(step_size))) if step_size < 1 else 0
    factor = 1 / step_size
    quantized = math.floor(round(value * factor, 8)) / factor
    return round(quantized, precision)

class InputValidator:
    """
    Validates order parameters against Binance Futures symbol rules (tickSize, stepSize, minQty).
    """
    def __init__(self, client: Optional[BinanceClient] = None):
        self.client = client
        self._exchange_info_cache: Optional[Dict[str, Any]] = None

    def _get_exchange_info(self) -> Dict[str, Any]:
        if self._exchange_info_cache is None and self.client is not None:
            try:
                self._exchange_info_cache = self.client.get_exchange_info()
            except Exception as e:
                logger.warning(f"Could not fetch exchangeInfo from Binance API: {e}. Falling back to default validation.")
                self._exchange_info_cache = {}
        return self._exchange_info_cache or {}

    def get_symbol_filters(self, symbol: str) -> Dict[str, float]:
        """
        Extracts tickSize, stepSize, minQty, and minNotional for a symbol from exchangeInfo.
        """
        info = self._get_exchange_info()
        symbols = info.get("symbols", [])
        
        for s in symbols:
            if s.get("symbol") == symbol.upper():
                filters = {f["filterType"]: f for f in s.get("filters", [])}
                price_filter = filters.get("PRICE_FILTER", {})
                lot_size_filter = filters.get("LOT_SIZE", {})
                min_notional_filter = filters.get("MIN_NOTIONAL", {})

                return {
                    "tickSize": float(price_filter.get("tickSize", "0.01")),
                    "stepSize": float(lot_size_filter.get("stepSize", "0.001")),
                    "minQty": float(lot_size_filter.get("minQty", "0.001")),
                    "minNotional": float(min_notional_filter.get("notional", "5.0")),
                }

        # Default fallback filters if offline or symbol not found in exchangeInfo
        return {
            "tickSize": 0.01,
            "stepSize": 0.001,
            "minQty": 0.001,
            "minNotional": 5.0,
        }

    def validate_symbol(self, symbol: str) -> str:
        """
        Ensures symbol is non-empty and uppercase alphanumeric.
        """
        if not symbol or not isinstance(symbol, str):
            raise ValidationError("Symbol must be a non-empty string.")
        
        symbol_clean = symbol.strip().upper()
        if not re.match(r"^[A-Z0-9-]{5,15}$", symbol_clean):
            raise ValidationError(f"Invalid symbol format: '{symbol}'. Expected format like 'BTCUSDT'.")
        
        return symbol_clean

    def validate_side(self, side: str) -> str:
        """
        Ensures side is either BUY or SELL.
        """
        if not side or not isinstance(side, str):
            raise ValidationError("Side must be 'BUY' or 'SELL'.")
        
        side_clean = side.strip().upper()
        if side_clean not in ("BUY", "SELL"):
            raise ValidationError(f"Invalid order side: '{side}'. Must be 'BUY' or 'SELL'.")
        
        return side_clean

    def validate_and_format(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: Optional[float] = None,
        stop_price: Optional[float] = None
    ) -> Tuple[str, str, float, Optional[float], Optional[float]]:
        """
        Validates all order inputs and formats quantity and price to symbol precision.
        """
        clean_symbol = self.validate_symbol(symbol)
        clean_side = self.validate_side(side)

        if quantity <= 0:
            raise ValidationError(f"Quantity must be greater than 0. Got {quantity}.")

        filters = self.get_symbol_filters(clean_symbol)
        
        # Validate quantity against minQty
        if quantity < filters["minQty"]:
            raise ValidationError(f"Quantity {quantity} is below minimum allowed quantity {filters['minQty']} for {clean_symbol}.")

        formatted_quantity = round_to_step_size(quantity, filters["stepSize"])

        formatted_price = None
        if price is not None:
            if price <= 0:
                raise ValidationError(f"Price must be greater than 0. Got {price}.")
            formatted_price = round_to_step_size(price, filters["tickSize"])

        formatted_stop_price = None
        if stop_price is not None:
            if stop_price <= 0:
                raise ValidationError(f"Stop price must be greater than 0. Got {stop_price}.")
            formatted_stop_price = round_to_step_size(stop_price, filters["tickSize"])

        logger.info(f"Validation Passed: {clean_symbol} {clean_side} Qty: {formatted_quantity} Price: {formatted_price}")
        return clean_symbol, clean_side, formatted_quantity, formatted_price, formatted_stop_price
