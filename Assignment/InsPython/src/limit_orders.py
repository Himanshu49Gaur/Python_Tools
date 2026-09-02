import argparse
import json
import os
import sys

# Ensure project root is in sys.path when script is executed directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.client import BinanceClient, BinanceAPIError
from src.validator import InputValidator, ValidationError
from src.logger import logger

def execute_limit_order(symbol: str, side: str, quantity: float, price: float, time_in_force: str = "GTC") -> dict:
    """
    Validates inputs and places a Limit Order on Binance USDT-M Futures.
    """
    logger.info(f"Initiating Limit Order execution for {symbol} {side} {quantity} @ {price}")
    
    client = BinanceClient()
    validator = InputValidator(client)

    # Validate parameters
    clean_symbol, clean_side, clean_qty, clean_price, _ = validator.validate_and_format(
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=price
    )

    if clean_price is None:
        raise ValidationError("Limit order requires a valid target price.")

    # Execute Order
    try:
        response = client.place_order(
            symbol=clean_symbol,
            side=clean_side,
            order_type="LIMIT",
            quantity=clean_qty,
            price=clean_price,
            time_in_force=time_in_force
        )
        logger.info(f"Limit Order Executed Successfully. OrderID: {response.get('orderId')}")
        return response
    except BinanceAPIError as e:
        logger.error(f"Limit Order Placement Failed: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Place a Limit Order on Binance USDT-M Futures.")
    parser.add_argument("symbol", type=str, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("side", type=str, choices=["BUY", "SELL", "buy", "sell"], help="Order side (BUY or SELL)")
    parser.add_argument("quantity", type=float, help="Order quantity")
    parser.add_argument("price", type=float, help="Limit price")
    parser.add_argument("--time_in_force", type=str, default="GTC", choices=["GTC", "IOC", "FOK"], help="Time in force (default: GTC)")

    args = parser.parse_args()

    try:
        result = execute_limit_order(
            symbol=args.symbol,
            side=args.side,
            quantity=args.quantity,
            price=args.price,
            time_in_force=args.time_in_force
        )
        print("\n=== Limit Order Result ===")
        print(json.dumps(result, indent=2))
    except (ValidationError, BinanceAPIError, Exception) as e:
        print(f"\n[ERROR] Order Execution Failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
