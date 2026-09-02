import argparse
import json
import os
import sys
import time
from typing import Dict, Any

# Ensure project root is in sys.path when script is executed directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.client import BinanceClient, BinanceAPIError
from src.validator import InputValidator, ValidationError
from src.logger import logger

def execute_oco_orders(
    symbol: str,
    side: str,
    quantity: float,
    take_profit_price: float,
    stop_loss_price: float,
    poll_interval: int = 3,
    max_polls: int = 100
) -> Dict[str, Any]:
    """
    Executes a One-Cancels-the-Other (OCO) order strategy on Binance USDT-M Futures.
    Places a Take-Profit order and a Stop-Loss order simultaneously.
    Monitors execution; if one order fills, the other is automatically cancelled.
    """
    logger.info(f"Initiating OCO Orders: {symbol} {side} Qty: {quantity} TP: {take_profit_price} SL: {stop_loss_price}")

    client = BinanceClient()
    validator = InputValidator(client)

    clean_symbol, clean_side, clean_qty, clean_tp, clean_sl = validator.validate_and_format(
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=take_profit_price,
        stop_price=stop_loss_price
    )

    if clean_tp is None or clean_sl is None:
        raise ValidationError("OCO orders require both take-profit price and stop-loss price.")

    # Leg 1: Take-Profit Limit Order
    logger.info(f"Placing OCO Leg 1 (Take Profit Limit): {clean_tp}")
    tp_order = client.place_order(
        symbol=clean_symbol,
        side=clean_side,
        order_type="LIMIT",
        quantity=clean_qty,
        price=clean_tp,
        time_in_force="GTC"
    )
    tp_order_id = tp_order.get("orderId")

    # Leg 2: Stop-Loss Market Order
    logger.info(f"Placing OCO Leg 2 (Stop Loss Market): {clean_sl}")
    sl_order = client.place_order(
        symbol=clean_symbol,
        side=clean_side,
        order_type="STOP_MARKET",
        quantity=clean_qty,
        stop_price=clean_sl
    )
    sl_order_id = sl_order.get("orderId")

    logger.info(f"OCO Placed Successfully. Leg 1 (TP OrderID: {tp_order_id}), Leg 2 (SL OrderID: {sl_order_id})")

    result = {
        "symbol": clean_symbol,
        "take_profit_order": tp_order,
        "stop_loss_order": sl_order,
        "status": "MONITORING"
    }

    # Monitoring Loop: Poll open orders to detect execution
    logger.info(f"Starting OCO monitoring loop (Polling every {poll_interval}s up to {max_polls} times)...")
    
    for poll_count in range(max_polls):
        time.sleep(poll_interval)
        try:
            open_orders = client.get_open_orders(clean_symbol)
            open_order_ids = [o["orderId"] for o in open_orders]

            tp_active = tp_order_id in open_order_ids
            sl_active = sl_order_id in open_order_ids

            if not tp_active and sl_active:
                logger.info(f"Take-Profit Order {tp_order_id} filled/triggered. Cancelling Stop-Loss Order {sl_order_id}...")
                client.cancel_order(clean_symbol, sl_order_id)
                result["status"] = "TAKE_PROFIT_FILLED_SL_CANCELLED"
                break
            elif not sl_active and tp_active:
                logger.info(f"Stop-Loss Order {sl_order_id} filled/triggered. Cancelling Take-Profit Order {tp_order_id}...")
                client.cancel_order(clean_symbol, tp_order_id)
                result["status"] = "STOP_LOSS_FILLED_TP_CANCELLED"
                break
            elif not tp_active and not sl_active:
                logger.info("Both OCO legs closed or executed.")
                result["status"] = "BOTH_CLOSED"
                break

        except BinanceAPIError as e:
            logger.warning(f"Error during OCO monitoring poll #{poll_count + 1}: {e}")

    return result

def main():
    parser = argparse.ArgumentParser(description="Place an OCO (One-Cancels-the-Other) order set on Binance USDT-M Futures.")
    parser.add_argument("symbol", type=str, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("side", type=str, choices=["BUY", "SELL", "buy", "sell"], help="Order side (BUY or SELL)")
    parser.add_argument("quantity", type=float, help="Order quantity")
    parser.add_argument("take_profit_price", type=float, help="Take Profit target price")
    parser.add_argument("stop_loss_price", type=float, help="Stop Loss trigger price")
    parser.add_argument("--poll_interval", type=int, default=3, help="Polling interval in seconds (default: 3)")

    args = parser.parse_args()

    try:
        result = execute_oco_orders(
            symbol=args.symbol,
            side=args.side,
            quantity=args.quantity,
            take_profit_price=args.take_profit_price,
            stop_loss_price=args.stop_loss_price,
            poll_interval=args.poll_interval
        )
        print("\n=== OCO Order Result ===")
        print(json.dumps(result, indent=2))
    except (ValidationError, BinanceAPIError, Exception) as e:
        print(f"\n[ERROR] OCO Execution Failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
