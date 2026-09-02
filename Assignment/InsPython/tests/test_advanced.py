import pytest
from src.validator import ValidationError
from src.advanced.twap import execute_twap_strategy
from src.advanced.grid_strategy import execute_grid_strategy
from src.advanced.fear_greed import calculate_risk_multiplier

def test_risk_multiplier_calculation():
    assert calculate_risk_multiplier(15) == 0.7   # Extreme Fear
    assert calculate_risk_multiplier(50) == 1.0   # Neutral
    assert calculate_risk_multiplier(85) == 0.5   # Extreme Greed

def test_twap_validation_errors():
    with pytest.raises(ValidationError):
        execute_twap_strategy("BTCUSDT", "BUY", total_quantity=1.0, duration_minutes=0, num_chunks=5)

    with pytest.raises(ValidationError):
        execute_twap_strategy("BTCUSDT", "BUY", total_quantity=1.0, duration_minutes=10, num_chunks=0)

def test_grid_validation_errors():
    # Lower price >= Upper price
    with pytest.raises(ValidationError):
        execute_grid_strategy("BTCUSDT", lower_price=60000, upper_price=50000, grid_levels=5, total_quantity=0.1)

    # Grid levels < 2
    with pytest.raises(ValidationError):
        execute_grid_strategy("BTCUSDT", lower_price=50000, upper_price=60000, grid_levels=1, total_quantity=0.1)
