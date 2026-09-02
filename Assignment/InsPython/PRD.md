# Product Requirement Document (PRD): Binance Futures Order Bot

## 1. Executive Summary & Objective

### 1.1 Objective
The objective of this project is to design, develop, and deliver a robust, modular, CLI-based trading bot for **Binance USDT-M Futures**. The bot enables traders to execute basic orders (Market, Limit) and advanced algorithmic strategy orders (Stop-Limit, OCO, TWAP, Grid Orders) with built-in input validation, structured logging, error handling, and optional market sentiment integration (Fear & Greed Index).

### 1.2 Target Audience
- Evaluation team / Instructors analyzing code quality, architecture, error handling, and financial logic.
- Algorithmic traders requiring a reliable CLI tool to execute futures orders on Binance.

---

## 2. Project Scope & Requirements Breakdown

### 2.1 Core Order Types (Mandatory - 50% Weight)
| Order Type | Description | CLI Arguments | Validation Rules |
| :--- | :--- | :--- | :--- |
| **Market Order** | Instant order execution at current best available market price. | `<symbol> <side> <quantity>` | Valid symbol, non-zero positive quantity, sufficient margin. |
| **Limit Order** | Order placed in order book to execute at target price or better. | `<symbol> <side> <quantity> <price>` | Target price must be within reasonable threshold of current mark price. |

### 2.2 Advanced Order Types (Bonus - 30% Weight)
| Order Strategy | Description | Key Parameters | Implementation File |
| :--- | :--- | :--- | :--- |
| **Stop-Limit Order** | Triggers a Limit Order when market price hits a designated Stop Price. | `stop_price`, `limit_price`, `quantity`, `side` | `src/advanced/stop_limit.py` |
| **OCO Order** | One-Cancels-the-Other: Combines Take-Profit and Stop-Loss orders; execution of one cancels the other. | `tp_price`, `sl_trigger_price`, `sl_limit_price`, `quantity` | `src/advanced/oco.py` |
| **TWAP Strategy** | Time-Weighted Average Price: Splits large order into `N` smaller chunks executed at regular time intervals `T`. | `total_quantity`, `duration_minutes`, `num_chunks` | `src/advanced/twap.py` |
| **Grid Orders** | Automated grid trading: Places buy-low and sell-high limit orders within a defined price range. | `lower_price`, `upper_price`, `grid_levels`, `total_qty` | `src/advanced/grid_strategy.py` |

### 2.3 Bonus Integration: Fear & Greed Index
- **Feature**: Fetch real-time market sentiment data from the Crypto Fear & Greed Index.
- **Use Case**: Dynamic risk control or conditional order execution (e.g., reduce grid position size during Extreme Fear / Extreme Greed).

---

## 3. Validation, Error Handling & Logging (10% Weight)

### 3.1 Input Validation Framework
- **Symbol Validation**: Check symbol against active Binance USDT-M Futures contracts (e.g., `BTCUSDT`, `ETHUSDT`).
- **Quantity & Price Precision**: Format parameters to match symbol-specific `stepSize` and `tickSize` rules from Binance `exchangeInfo`.
- **Side & Order Type Verification**: Ensure `side` is strictly `BUY` or `SELL`.
- **Margin & Leverage Check**: Verify initial account margin prior to API dispatch.

### 3.2 Structured Logging (`bot.log`)
- **Format**: JSON or structured plain text with standard ISO timestamps (`YYYY-MM-DD HH:MM:SS,ms`), log level (`INFO`, `WARNING`, `ERROR`), component, and context.
- **Scope**:
  - API request & response payloads (with sensitive API secrets redacted).
  - Order state changes (Created, Pending, Filled, Cancelled, Rejected).
  - Full exception tracebacks for network or API errors (e.g., code -2019 `MARGIN_INSUFFICIENT`).

---

## 4. Technical Architecture & File Structure

### 4.1 Recommended Directory Tree
```text
[project_root]/
│
├── src/                          # Application Source Code
│   ├── __init__.py
│   ├── config.py                 # Configuration loader (API keys, testnet endpoints)
│   ├── client.py                 # Binance Futures API client wrapper & auth
│   ├── validator.py              # Input validation and precision utilities
│   ├── logger.py                 # Structured logging setup
│   ├── market_orders.py          # Market order CLI endpoint
│   ├── limit_orders.py           # Limit order CLI endpoint
│   └── advanced/                 # Advanced order strategies module
│       ├── __init__.py
│       ├── stop_limit.py         # Stop-limit order logic
│       ├── oco.py                # OCO order logic
│       ├── twap.py               # TWAP strategy executor
│       ├── grid_strategy.py      # Grid trading algorithm
│       └── fear_greed.py         # Fear & Greed Index integration
│
├── .env.example                  # Environment variable template
├── bot.log                       # Generated runtime log file
├── report.pdf                    # Execution screenshots, performance analysis & strategy writeup
├── README.md                     # Setup instructions, API guide & execution commands
└── requirements.txt              # Python dependencies (python-binance, requests, python-dotenv)
```

---

## 5. Non-Functional Requirements

### 5.1 Security
- **Credential Protection**: API keys and secrets stored strictly in environment variables (`.env`). No hardcoded secrets.
- **Sanitization**: API keys and authorization headers masked in log outputs.

### 5.2 Environment & Testnet Support
- **Support**: Native switching between Binance Futures Testnet (`https://testnet.binancefuture.com`) and Production via `.env` configuration (`USE_TESTNET=true`).

### 5.3 Code Quality & Reproducibility
- Descriptive modular filenames (no generic names like `task1.py`).
- Clean PEP8-compliant Python code with type hints and docstrings.
- Fully reproducible setup instructions in `README.md`.

---

## 6. Evaluation Criteria & Deliverables Matrix

| Criteria | Weight | Requirements to Achieve Max Score |
| :--- | :--- | :--- |
| **Basic Orders** | 50% | Complete execution of Market and Limit orders on USDT-M Futures with full input validation and error feedback. |
| **Advanced Orders** | 30% | Working implementations of Stop-Limit, OCO, TWAP, and Grid orders; dynamic execution with error recovery. |
| **Logging & Errors** | 10% | Clean, structured `bot.log` recording all API calls, order lifecycle events, and detailed error tracebacks. |
| **Report & Documentation**| 10% | Professional `README.md` with clear CLI commands, plus a comprehensive `report.pdf` featuring execution evidence and screenshots. |

---

## 7. Submission Checklist & Deliverables
1. **GitHub Repository**:
   - Private repository named `[your_name]-binance-bot` (e.g., `alice-binance-bot`).
   - Collaborators added per instructor guidelines.
2. **Archive File**:
   - Single `.zip` archive named `[your_name]_binance_bot.zip` matching repository structure.
