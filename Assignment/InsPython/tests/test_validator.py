import pytest
from src.validator import InputValidator, ValidationError, round_to_step_size

def test_round_to_step_size():
    assert round_to_step_size(0.0126, 0.001) == 0.012
    assert round_to_step_size(105.489, 0.1) == 105.4
    assert round_to_step_size(50.0, 1.0) == 50.0

def test_validate_symbol():
    validator = InputValidator()
    assert validator.validate_symbol("btcusdt") == "BTCUSDT"
    assert validator.validate_symbol("ETHUSDT") == "ETHUSDT"

    with pytest.raises(ValidationError):
        validator.validate_symbol("INVALID_SYMBOL_TOO_LONG_1234567")

    with pytest.raises(ValidationError):
        validator.validate_symbol("")

def test_validate_side():
    validator = InputValidator()
    assert validator.validate_side("buy") == "BUY"
    assert validator.validate_side("SELL") == "SELL"

    with pytest.raises(ValidationError):
        validator.validate_side("HOLD")

def test_validate_and_format_quantity():
    validator = InputValidator()
    
    # Valid params
    symbol, side, qty, price, _ = validator.validate_and_format("BTCUSDT", "BUY", 0.0126, price=60000.45)
    assert symbol == "BTCUSDT"
    assert side == "BUY"
    assert qty == 0.012
    assert price == 60000.45

    # Invalid negative quantity
    with pytest.raises(ValidationError):
        validator.validate_and_format("BTCUSDT", "BUY", -1.0)
