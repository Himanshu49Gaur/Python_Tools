# Project Execution Plan: Binance Futures Order Bot (3 Phases)

Based on the **Assignment Instructions**, **PRD**, and **TRD**, the implementation is structured into 3 distinct, milestone-driven phases.

---

## Phase 1: Core Architecture, Infrastructure & Basic Orders (Mandatory - 50% Weight)

### Key Objectives
Establish the foundational framework, environment configuration, secure API wrapper, input validator, structured logging engine, and mandatory CLI order types (Market & Limit).

### Deliverables
1. **Environment & Configuration (`src/config.py`)**:
   - Environment variable loader using `.env`.
   - Support for Binance USDT-M Futures Testnet (`https://testnet.binancefuture.com`) & Production.
2. **API Client & Authentication Facade (`src/client.py`)**:
   - HMAC-SHA256 signature generator for signed REST endpoints.
   - HTTP request wrapper with exponential backoff retry policy.
3. **Validation & Precision Subsystem (`src/validator.py`)**:
   - Cache `exchangeInfo` rules (`tickSize`, `stepSize`, `minQty`, `notional`).
   - Precision rounding routines for prices and quantities.
   - Input sanitizer for symbols (`BTCUSDT`, etc.) and side (`BUY`/`SELL`).
4. **Structured Logging System (`src/logger.py`)**:
   - Centralized logging to `bot.log` and stdout.
   - Sensitive data redactor filter (protecting API keys and signatures).
5. **Core CLI Order Modules**:
   - `src/market_orders.py`: Command-line execution for Market Orders.
   - `src/limit_orders.py`: Command-line execution for Limit Orders.
6. **Unit Tests**:
   - Initial `pytest` suite for validator and client signing logic.

---

## Phase 2: Advanced Order Strategies & Bonus Integrations (Bonus - 30% Weight)

### Key Objectives
Develop automated algorithmic trading strategies, execution state listeners, order management engines, and external market sentiment integration.

### Deliverables
1. **Stop-Limit Orders (`src/advanced/stop_limit.py`)**:
   - Logic to place conditional stop-limit orders triggering on stop price hit.
2. **OCO (One-Cancels-the-Other) Engine (`src/advanced/oco.py`)**:
   - Simultaneous Take-Profit Limit and Stop-Loss Market order dispatcher.
   - Async background monitor to cancel remaining leg upon execution of one.
3. **TWAP (Time-Weighted Average Price) Strategy (`src/advanced/twap.py`)**:
   - Algorithm to divide total quantity into `N` chunks executed at fixed time intervals `T`.
4. **Grid Trading Strategy (`src/advanced/grid_strategy.py`)**:
   - Multi-level grid calculation engine placing buy-low / sell-high limit orders within a defined price channel.
5. **Fear & Greed Index Integration (`src/advanced/fear_greed.py`)**:
   - API client fetching Crypto Fear & Greed sentiment to dynamically scale order sizing/risk.

---

## Phase 3: Verification, Logging Audit, Documentation & Deliverables (20% Weight)

### Key Objectives
Validate system behavior end-to-end on Binance Testnet, ensure structured log accuracy, generate comprehensive documentation, and prepare submission archives.

### Deliverables
1. **End-to-End Testnet Verification**:
   - Execute test cases across all order types (Market, Limit, Stop-Limit, OCO, TWAP, Grid).
   - Capture execution logs and console outputs.
2. **Logging Audit & Verification (`bot.log`)**:
   - Verify timestamp formatting, API payloads, execution state transitions, and error tracebacks.
3. **Documentation Package**:
   - `README.md`: Complete setup guide, API configuration, CLI usage examples, dependency specifications.
   - `report.pdf` (or detailed strategy report): Execution screenshots, architectural write-up, test evidence.
4. **Final Deliverable Packaging**:
   - GitHub Repository configuration (`[your_name]-binance-bot`).
   - Deliverable archive generation (`[your_name]_binance_bot.zip`).

---

## Summary Matrix

| Phase | Core Focus | Criteria Weight | Target Output Files |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Setup, API Auth, Logging, Validator, Market & Limit Orders | **50%** | `config.py`, `client.py`, `validator.py`, `logger.py`, `market_orders.py`, `limit_orders.py` |
| **Phase 2** | Stop-Limit, OCO, TWAP, Grid Orders, Fear & Greed Integration | **30%** | `stop_limit.py`, `oco.py`, `twap.py`, `grid_strategy.py`, `fear_greed.py` |
| **Phase 3** | Testnet Verification, `bot.log` Audit, `README.md`, `report.pdf`, `.zip` Archive | **20%** | `README.md`, `report.pdf`, `bot.log`, `[your_name]_binance_bot.zip` |
