import argparse
import json
import os
import sys
import requests
from typing import Dict, Any

# Ensure project root is in sys.path when script is executed directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.logger import logger

FEAR_GREED_API_URL = "https://api.alternative.me/fng/?limit=1"

def fetch_fear_and_greed_index() -> Dict[str, Any]:
    """
    Fetches real-time Crypto Fear & Greed Index data.
    """
    logger.info("Fetching Crypto Fear & Greed Index data...")
    try:
        response = requests.get(FEAR_GREED_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        item = data["data"][0]
        
        value = int(item["value"])
        classification = item["value_classification"]

        logger.info(f"Fear & Greed Index: {value} ({classification})")
        return {
            "value": value,
            "classification": classification,
            "timestamp": item.get("timestamp")
        }
    except Exception as e:
        logger.error(f"Failed to fetch Fear & Greed Index: {e}")
        # Default fallback neutral index
        return {
            "value": 50,
            "classification": "Neutral (Fallback)",
            "timestamp": None
        }

def calculate_risk_multiplier(index_value: int) -> float:
    """
    Calculates dynamic risk/position multiplier based on Fear & Greed Index value (0-100).
    - Extreme Fear (0-25): Reduce position size to 0.7x (high volatility risk).
    - Fear (26-45): Normal 1.0x sizing.
    - Neutral (46-55): Normal 1.0x sizing.
    - Greed (56-75): 1.0x sizing.
    - Extreme Greed (76-100): Reduce position size to 0.5x (overbought reversal risk).
    """
    if index_value <= 25:
        return 0.7
    elif index_value >= 76:
        return 0.5
    else:
        return 1.0

def main():
    parser = argparse.ArgumentParser(description="Fetch Crypto Fear & Greed Index and calculate sentiment risk multiplier.")
    args = parser.parse_args()

    sentiment = fetch_fear_and_greed_index()
    multiplier = calculate_risk_multiplier(sentiment["value"])

    output = {
        "sentiment": sentiment,
        "recommended_risk_multiplier": multiplier,
        "guidance": f"Position sizing scaled by {multiplier}x due to market classification '{sentiment['classification']}'."
    }

    print("\n=== Crypto Fear & Greed Sentiment Analysis ===")
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
