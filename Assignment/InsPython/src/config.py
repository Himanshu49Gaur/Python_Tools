import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

PROD_BASE_URL = "https://fapi.binance.com"
TESTNET_BASE_URL = "https://testnet.binancefuture.com"

@dataclass
class Config:
    api_key: str
    api_secret: str
    use_testnet: bool
    base_url: str

def load_config() -> Config:
    """
    Loads configuration settings from environment variables.
    """
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()
    use_testnet_str = os.getenv("USE_TESTNET", "true").strip().lower()
    use_testnet = use_testnet_str in ("true", "1", "yes")
    
    base_url = TESTNET_BASE_URL if use_testnet else PROD_BASE_URL

    return Config(
        api_key=api_key,
        api_secret=api_secret,
        use_testnet=use_testnet,
        base_url=base_url
    )
