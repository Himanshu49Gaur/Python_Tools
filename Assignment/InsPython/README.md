# Binance Futures Order Bot

A modular, high-performance CLI trading bot for **Binance USDT-M Futures** built in Python. Features support for basic orders (Market, Limit), advanced algorithmic execution strategies (Stop-Limit, OCO, TWAP, Grid), strict input validation, credential sanitization, structured logging, and market sentiment analysis via the Crypto Fear & Greed Index.

---

## 1. Features & Capabilities

- **Core Orders (Mandatory)**:
  - **Market Orders**: Instant execution at current market price.
  - **Limit Orders**: Order placement at specified price targets with custom Time-in-Force (`GTC`, `IOC`, `FOK`).
- **Advanced Strategies (Bonus)**:
  - **Stop-Limit Orders**: Trigger limit orders automatically when stop prices are crossed.
  - **OCO (One-Cancels-the-Other)**: Simultaneous Take-Profit and Stop-Loss orders with a background execution listener that cancels the open leg when one fills.
  - **TWAP (Time-Weighted Average Price)**: Algorithmic chunking of large orders across fixed time intervals.
  - **Grid Orders**: Automated buy-low / sell-high grid matrix across a defined price channel.
  - **Fear & Greed Index Integration**: Live sentiment API integration to dynamically adjust position risk multipliers.
- **Validation & Safety**:
  - Symbol format and existence checks.
  - Automatic precision quantization matching Binance `tickSize` and `stepSize` rules.
  - Quantity and boundary verification against `minQty` constraints.
- **Logging & Security**:
  - Structured logging to both console and `bot.log`.
  - Built-in `RedactSensitiveFilter` redacting API keys, secrets, and HMAC signatures from log streams.

---

## 2. File Structure

```text
[project_root]/
├── src/                          # Application source code
│   ├── __init__.py
│   ├── config.py                 # Environment configuration loader
│   ├── client.py                 # Binance Futures API client facade & HMAC signing
│   ├── validator.py              # Precision quantization & parameter validator
│   ├── logger.py                 # Structured logger with credential redactor
│   ├── market_orders.py          # Market order CLI endpoint
│   ├── limit_orders.py           # Limit order CLI endpoint
│   └── advanced/                 # Advanced algorithmic strategy engines
│       ├── __init__.py
│       ├── stop_limit.py         # Stop-limit execution module
│       ├── oco.py                # OCO order pair listener & execution engine
│       ├── twap.py               # TWAP time-chunking execution engine
│       ├── grid_strategy.py      # Multi-level grid trading engine
│       └── fear_greed.py         # Crypto Fear & Greed sentiment integration
├── tests/                        # Automated unit & integration test suite
│   ├── __init__.py
│   ├── test_client.py            # Client auth & logging filter tests
│   ├── test_validator.py         # Precision math & parameter validation tests
│   └── test_advanced.py          # Strategy chunking & grid level math tests
├── .env.example                  # Template environment file
├── bot.log                       # Structured application log file
├── report.pdf                    # Execution analysis report & screenshots
├── README.md                     # Documentation & usage guide
└── requirements.txt              # Project dependencies
```

---

## 3. Installation & Setup

### 3.1 Prerequisites
- Python `3.10` or higher installed.
- Binance Futures Testnet or Production API Credentials.

### 3.2 Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/your_name-binance-bot.git
   cd your_name-binance-bot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and enter your Binance Futures API Key and Secret.
   ```bash
   cp .env.example .env
   ```

   Edit `.env`:
   ```env
   BINANCE_API_KEY=your_actual_binance_api_key
   BINANCE_API_SECRET=your_actual_binance_api_secret
   USE_TESTNET=true
   ```

---

## 4. Usage Guide & CLI Commands

### 4.1 Basic Orders

#### Market Order
Executes a Market Order immediately.
```bash
python src/market_orders.py BTCUSDT BUY 0.01
```

#### Limit Order
Places a Limit Order at a target price.
```bash
python src/limit_orders.py BTCUSDT BUY 0.01 60000 --time_in_force GTC
```

---

### 4.2 Advanced Orders & Strategies

#### Stop-Limit Order
Triggers a Limit Order at `price` when market hits `stop_price`.
```bash
python src/advanced/stop_limit.py BTCUSDT BUY 0.01 59000 59500
```

#### OCO (One-Cancels-the-Other) Order
Places linked Take-Profit and Stop-Loss orders. Listens for execution and cancels remaining order.
```bash
python src/advanced/oco.py BTCUSDT BUY 0.01 65000 58000
```

#### TWAP (Time-Weighted Average Price) Strategy
Splits `0.05` BTC into `5` chunks executed over `10` minutes.
```bash
python src/advanced/twap.py BTCUSDT BUY 0.05 10 5
```

#### Grid Trading Strategy
Deploys `5` buy/sell grid levels between `$55,000` and `$65,000` for a total of `0.05` BTC.
```bash
python src/advanced/grid_strategy.py BTCUSDT 55000 65000 5 0.05
```

#### Fear & Greed Index Market Sentiment
Fetches live sentiment index and outputs position risk multiplier.
```bash
python src/advanced/fear_greed.py
```

---

## 5. Running Automated Tests

Run the full pytest suite to verify validation logic, precision rounding, HMAC signature generation, and strategy math:
```bash
python -m pytest tests/
```

---

## 6. Submission Guidelines

To submit this project:
1. Push code to a private GitHub repository named `[your_name]-binance-bot`.
2. Add your instructor as a collaborator.
3. Zip the project root directory as `[your_name]_binance_bot.zip`.
