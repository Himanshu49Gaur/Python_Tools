import hmac
import hashlib
import time
import requests
from typing import Dict, Any, Optional
from urllib.parse import urlencode

from src.config import Config, load_config
from src.logger import logger

class BinanceAPIError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"Binance API Error [{code}]: {message}")

class BinanceClient:
    """
    Binance USDT-M Futures REST API Client wrapper handling authentication,
    signing, and error handling.
    """
    def __init__(self, config: Optional[Config] = None):
        self.config = config or load_config()
        self.session = requests.Session()
        if self.config.api_key:
            self.session.headers.update({"X-MBX-APIKEY": self.config.api_key})

    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """
        Generates HMAC-SHA256 signature for signed endpoints.
        """
        query_string = urlencode(params)
        return hmac.new(
            self.config.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def _request(self, method: str, endpoint: str, signed: bool = False, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes HTTP request to Binance Futures API.
        """
        url = f"{self.config.base_url}{endpoint}"
        params = params or {}

        if signed:
            if not self.config.api_key or not self.config.api_secret:
                raise ValueError("API Key and Secret must be configured for signed requests.")
            params["timestamp"] = int(time.time() * 1000)
            params["signature"] = self._generate_signature(params)

        logger.info(f"API Request: {method.upper()} {endpoint} | Params: {params}")

        try:
            response = self.session.request(method, url, params=params, timeout=10)
            data = response.json()

            if response.status_code >= 400:
                code = data.get("code", response.status_code)
                msg = data.get("msg", response.text)
                logger.error(f"API Request Failed: {endpoint} | Code: {code} | Msg: {msg}")
                raise BinanceAPIError(code, msg)

            logger.info(f"API Response Success: {endpoint}")
            return data

        except requests.RequestException as e:
            logger.error(f"Network error during API request to {endpoint}: {e}")
            raise

    # Public Endpoints
    def get_exchange_info(self) -> Dict[str, Any]:
        """
        Fetches exchange trading rules and symbol information.
        """
        return self._request("GET", "/fapi/v1/exchangeInfo", signed=False)

    def get_mark_price(self, symbol: str) -> float:
        """
        Fetches mark price for a given symbol.
        """
        res = self._request("GET", "/fapi/v1/premiumIndex", signed=False, params={"symbol": symbol.upper()})
        return float(res["markPrice"])

    # Signed Account & Order Endpoints
    def get_account_info(self) -> Dict[str, Any]:
        """
        Queries account balance and margin statistics.
        """
        return self._request("GET", "/fapi/v2/account", signed=True)

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        stop_price: Optional[float] = None,
        time_in_force: str = "GTC"
    ) -> Dict[str, Any]:
        """
        Places an order on Binance Futures.
        """
        params: Dict[str, Any] = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity,
        }

        if order_type.upper() == "LIMIT":
            if price is None:
                raise ValueError("Limit orders require a price.")
            params["price"] = price
            params["timeInForce"] = time_in_force

        elif order_type.upper() in ("STOP", "STOP_MARKET"):
            if stop_price is None:
                raise ValueError("Stop orders require a stop_price.")
            params["stopPrice"] = stop_price
            if order_type.upper() == "STOP":
                if price is None:
                    raise ValueError("Stop Limit orders require a price.")
                params["price"] = price
                params["timeInForce"] = time_in_force

        logger.info(f"Placing Order: {side} {quantity} {symbol} @ {order_type} (Price: {price}, StopPrice: {stop_price})")
        return self._request("POST", "/fapi/v1/order", signed=True, params=params)

    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Cancels an active order by order ID.
        """
        params = {"symbol": symbol.upper(), "orderId": order_id}
        return self._request("DELETE", "/fapi/v1/order", signed=True, params=params)

    def get_open_orders(self, symbol: Optional[str] = None) -> Any:
        """
        Gets open orders for a specific symbol or all symbols.
        """
        params = {}
        if symbol:
            params["symbol"] = symbol.upper()
        return self._request("GET", "/fapi/v1/openOrders", signed=True, params=params)
