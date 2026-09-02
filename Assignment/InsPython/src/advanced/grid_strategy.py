import argparse
import json
import os
import sys
from typing import Dict, Any, List

# Ensure project root is in sys.path when script is executed directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.client import BinanceClient, BinanceAPIError
from src.validator import InputValidator, ValidationError, round_to_step_size
from src.logger import logger

def execute_grid_strategy(
    symbol: str,
    lower_price: float,
    upper_price: float,
    grid_levels: int,
    total_quantity: float
) -> Dict[str, Any]:
    """
    Executes a Grid Trading Strategy on Binance USDT-M Futures.
    Distributes buy-low and sell-high limit orders within [lower_price, upper_price].
    """
    if lower_price >= upper_price:
        raise ValidationError(f"Lower price ({lower_price}) must be strictly less than upper price ({upper_price}).")
    if grid_levels < 2:
        raise ValidationError("Grid levels must be at least 2.")
    if total_quantity <= 0:
        raise ValidationError("Total quantity must be greater than 0.")

    logger.info(f"Initiating Grid Strategy for {symbol}: Range [{lower_price} - {upper_price}], Levels: {grid_levels}, TotalQty: {total_quantity}")

    client = BinanceClient()
    validator = InputValidator(client)

    clean_symbol = validator.validate_symbol(symbol)
    filters = validator.get_symbol_filters(clean_symbol)

    raw_level_qty = total_quantity / grid_levels
    level_qty = round_to_step_size(raw_level_qty, filters["stepSize"])

    if level_qty < filters["minQty"]:
        raise ValidationError(f"Quantity per grid level ({level_qty}) is below minimum allowed ({filters['minQty']}) for {clean_symbol}.")

    # Fetch current market price to classify BUY vs SELL grid levels
    try:
        mark_price = client.get_mark_price(clean_symbol)
        logger.info(f"Current Mark Price for {clean_symbol}: {mark_price}")
    except Exception as e:
        logger.warning(f"Could not fetch mark price for {clean_symbol}: {e}. Using grid midpoint as reference.")
        mark_price = (lower_price + upper_price) / 2.0

    price_step = (upper_price - lower_price) / (grid_levels - 1)
    grid_orders: List[Dict[str, Any]] = []

    for i in range(grid_levels):
        raw_price = lower_price + (i * price_step)
        level_price = round_to_step_size(raw_price, filters["tickSize"])

        # Determine side based on position relative to current mark price
        if level_price < mark_price:
            side = "BUY"
        else:
            side = "SELL"

        logger.info(f"Placing Grid Order #{i+1}/{grid_levels}: {side} {level_qty} {clean_symbol} @ {level_price}")

        try:
            order_res = client.place_order(
                symbol=clean_symbol,
                side=side,
                order_type="LIMIT",
                quantity=level_qty,
                price=level_price,
                time_in_force="GTC"
            )
            grid_orders.append({
                "level": i + 1,
                "side": side,
                "price": level_price,
                "quantity": level_qty,
                "order": order_res
            })
        except BinanceAPIError as e:
            logger.error(f"Grid Level #{i+1} Order Failed: {e}")

    summary = {
        "symbol": clean_symbol,
        "lower_price": lower_price,
        "upper_price": upper_price,
        "grid_levels": grid_levels,
        "quantity_per_level": level_qty,
        "mark_price_reference": mark_price,
        "placed_orders_count": len(grid_orders),
        "grid_orders": grid_orders
    }

    logger.info(f"Grid Strategy Deployment Completed. {len(grid_orders)}/{grid_levels} orders active.")
    return summary

def main():
    parser = argparse.ArgumentParser(description="Deploy a Grid Trading strategy on Binance USDT-M Futures.")
    parser.add_argument("symbol", type=str, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("lower_price", type=float, help="Lower price boundary of grid")
    parser.add_argument("upper_price", type=float, help="Upper price boundary of grid")
    parser.add_argument("grid_levels", type=int, help="Number of grid price levels")
    parser.add_argument("total_quantity", type=float, help="Total quantity to distribute across grid")

    args = parser.parse_args()

    try:
        result = execute_grid_strategy(
            symbol=args.symbol,
            lower_price=args.lower_price,
            upper_price=args.upper_price,
            grid_levels=args.grid_levels,
            total_quantity=args.total_quantity
        )
        print("\n=== Grid Strategy Summary ===")
        print(json.dumps(result, indent=2))
    except (ValidationError, BinanceAPIError, Exception) as e:
        print(f"\n[ERROR] Grid Deployment Failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
