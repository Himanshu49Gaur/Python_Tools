import logging
from src.config import Config
from src.client import BinanceClient
from src.logger import RedactSensitiveFilter

def test_signature_generation():
    config = Config(
        api_key="test_key",
        api_secret="test_secret",
        use_testnet=True,
        base_url="https://testnet.binancefuture.com"
    )
    client = BinanceClient(config)
    params = {"symbol": "LTCBTC", "side": "BUY", "type": "LIMIT", "timeInForce": "GTC", "quantity": 1, "price": 0.1, "timestamp": 1499827319559}
    signature = client._generate_signature(params)
    assert isinstance(signature, str)
    assert len(signature) == 64  # SHA256 hex digest length

def test_redact_sensitive_filter():
    filter_obj = RedactSensitiveFilter()
    record = logging.LogRecord(
        name="test", level=logging.INFO, pathname="", lineno=0,
        msg="API call with X-MBX-APIKEY: 1234567890secretkey and signature=a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",
        args=(), exc_info=None
    )
    filter_obj.filter(record)
    assert "1234567890secretkey" not in record.msg
    assert "[REDACTED_API_KEY]" in record.msg
    assert "[REDACTED_SIGNATURE]" in record.msg
