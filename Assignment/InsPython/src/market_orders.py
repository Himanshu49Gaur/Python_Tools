import argparse
import json
import os
import sys

# Ensure project root is in sys.path when script is executed directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.client import BinanceClient, BinanceAPIError
from src.validator import InputValidator, ValidationError
from src.logger import logger

def execute_market_order(symbol: str, side: str, quantity: float) -> dict:
    """
    Validates inputs and places a Market Order on Binance USDT-M Futures.
    """
    logger.info(f"Initiating Market Order execution for {symbol} {side} {quantity}")
    
    client = BinanceClient()
    validator = InputValidator(client)

    # Validate parameters
    clean_symbol, clean_side, clean_qty, _, _ = validator.validate_and_format(
        symbol=symbol,
        side=side,
        quantity=quantity
    )

    # Execute Order
    try:
        response = client.place_order(
            symbol=clean_symbol,
            side=clean_side,
            order_type="MARKET",
            quantity=clean_qty
        )
        logger.info(f"Market Order Executed Successfully. OrderID: {response.get('orderId')}")
        return response
    except BinanceAPIError as e:
        logger.error(f"Market Order Placement Failed: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Place a Market Order on Binance USDT-M Futures.")
    parser.add_argument("symbol", type=str, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("side", type=str, choices=["BUY", "SELL", "buy", "sell"], help="Order side (BUY or SELL)")
    parser.add_argument("quantity", type=float, help="Order quantity")

    args = parser.parse_args()

    try:
        result = execute_market_order(
            symbol=args.symbol,
            side=args.side,
            quantity=args.quantity
        )
        print("\n=== Market Order Result ===")
        print(json.dumps(result, indent=2))
    except (ValidationError, BinanceAPIError, Exception) as e:
        print(f"\n[ERROR] Order Execution Failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
