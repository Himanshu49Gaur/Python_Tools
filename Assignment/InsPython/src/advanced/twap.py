import argparse
import json
import os
import sys
import time
from typing import Dict, Any, List

# Ensure project root is in sys.path when script is executed directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.client import BinanceClient, BinanceAPIError
from src.validator import InputValidator, ValidationError, round_to_step_size
from src.logger import logger

def execute_twap_strategy(
    symbol: str,
    side: str,
    total_quantity: float,
    duration_minutes: float,
    num_chunks: int,
    order_type: str = "MARKET",
    limit_price: float = None
) -> Dict[str, Any]:
    """
    Executes a Time-Weighted Average Price (TWAP) order strategy.
    Splits total_quantity into num_chunks placed over duration_minutes.
    """
    if num_chunks <= 0:
        raise ValidationError("Number of chunks must be greater than 0.")
    if duration_minutes <= 0:
        raise ValidationError("Duration must be greater than 0 minutes.")

    logger.info(f"Initiating TWAP Strategy: {symbol} {side} TotalQty: {total_quantity} over {duration_minutes} mins ({num_chunks} chunks)")

    client = BinanceClient()
    validator = InputValidator(client)

    clean_symbol, clean_side, clean_total_qty, clean_price, _ = validator.validate_and_format(
        symbol=symbol,
        side=side,
        quantity=total_quantity,
        price=limit_price
    )

    filters = validator.get_symbol_filters(clean_symbol)
    raw_chunk_qty = clean_total_qty / num_chunks
    chunk_qty = round_to_step_size(raw_chunk_qty, filters["stepSize"])

    if chunk_qty < filters["minQty"]:
        raise ValidationError(f"Chunk size {chunk_qty} is below minimum allowed quantity {filters['minQty']} for {clean_symbol}.")

    interval_seconds = (duration_minutes * 60.0) / num_chunks

    executed_orders: List[Dict[str, Any]] = []

    for chunk_idx in range(1, num_chunks + 1):
        logger.info(f"TWAP Executing Chunk {chunk_idx}/{num_chunks}: {clean_symbol} {clean_side} Qty: {chunk_qty}")

        try:
            order_res = client.place_order(
                symbol=clean_symbol,
                side=clean_side,
                order_type=order_type,
                quantity=chunk_qty,
                price=clean_price if order_type.upper() == "LIMIT" else None
            )
            executed_orders.append(order_res)
            logger.info(f"TWAP Chunk {chunk_idx} Executed. OrderID: {order_res.get('orderId')}")
        except BinanceAPIError as e:
            logger.error(f"TWAP Chunk {chunk_idx} Failed: {e}")

        # Sleep interval if not final chunk
        if chunk_idx < num_chunks:
            logger.info(f"TWAP Sleeping for {interval_seconds:.2f} seconds before next chunk...")
            time.sleep(interval_seconds)

    summary = {
        "symbol": clean_symbol,
        "side": clean_side,
        "total_requested_quantity": clean_total_qty,
        "num_chunks": num_chunks,
        "chunk_quantity": chunk_qty,
        "interval_seconds": interval_seconds,
        "executed_chunks_count": len(executed_orders),
        "orders": executed_orders
    }

    logger.info(f"TWAP Strategy Completed. Executed {len(executed_orders)}/{num_chunks} chunks.")
    return summary

def main():
    parser = argparse.ArgumentParser(description="Execute a TWAP (Time-Weighted Average Price) strategy on Binance USDT-M Futures.")
    parser.add_argument("symbol", type=str, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("side", type=str, choices=["BUY", "SELL", "buy", "sell"], help="Order side (BUY or SELL)")
    parser.add_argument("total_quantity", type=float, help="Total order quantity")
    parser.add_argument("duration_minutes", type=float, help="Total duration in minutes")
    parser.add_argument("num_chunks", type=int, help="Number of order chunks")
    parser.add_argument("--order_type", type=str, default="MARKET", choices=["MARKET", "LIMIT"], help="Chunk order type")
    parser.add_argument("--limit_price", type=float, default=None, help="Limit price (if order_type is LIMIT)")

    args = parser.parse_args()

    try:
        result = execute_twap_strategy(
            symbol=args.symbol,
            side=args.side,
            total_quantity=args.total_quantity,
            duration_minutes=args.duration_minutes,
            num_chunks=args.num_chunks,
            order_type=args.order_type,
            limit_price=args.limit_price
        )
        print("\n=== TWAP Execution Summary ===")
        print(json.dumps(result, indent=2))
    except (ValidationError, BinanceAPIError, Exception) as e:
        print(f"\n[ERROR] TWAP Execution Failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
