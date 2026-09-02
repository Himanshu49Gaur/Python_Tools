# Web3 Trading Analytics: Hyperliquid Trader Behavior vs. Bitcoin Market Sentiment

---

## Executive Summary
This candidate submission presents an end-to-end data science investigation analyzing the relationship between **Hyperliquid Perpetual DEX trader behavior** and **Bitcoin macro market sentiment (Fear & Greed Index)**.

By merging high-frequency trade execution logs with daily market sentiment scores, this project identifies behavioral biases, leverage risks, positioning tendencies across performance cohorts, and statistical signals for Web3 algorithmic execution strategies.

---

## Standardized Submission Structure

```
ds_<candidate_name>/
├── PRD.md                     # Product Requirements Document
├── TRD.md                     # Technical Requirements Document
├── README.md                  # Detailed Setup, Overview & Colab Link Instructions
├── notebook_1.ipynb           # Primary Google Colab Notebook (Preprocessing, Merging, Statistical Analysis & EDA)
├── notebook_2.ipynb           # Secondary Google Colab Notebook (Advanced Predictive Modeling & Strategy Backtesting)
├── ds_report.pdf              # Final Executive Technical Report (PDF with Embedded Visuals & Test Results)
├── csv_files/                 # Processed & Aggregated Data Outputs
│   ├── merged_trader_sentiment.csv
│   ├── daily_sentiment_metrics.csv
│   └── trader_cohort_summary.csv
└── outputs/                   # High-Resolution Publication Graphics (300 DPI)
    ├── pnl_vs_sentiment.png
    ├── leverage_distribution_by_regime.png
    ├── long_short_ratio_heatmap.png
    ├── winrate_by_cohort.png
    └── trade_volume_distribution.png
```

---

## Google Colab Links
*(To view or run the interactive notebooks in Google Colab, import `notebook_1.ipynb` or `notebook_2.ipynb` into Colab or open via GitHub)*

* **Notebook 1 (Core Analysis & EDA):** `[Colab Link Placeholder - Set permissions to 'Anyone with the link can view']`
* **Notebook 2 (Backtesting & Modeling):** `[Colab Link Placeholder - Set permissions to 'Anyone with the link can view']`

---

## Key Findings & Statistical Verification

1. **H1 (Leverage Escalation):** Retail and underperforming accounts increase average position leverage during `Extreme Greed` regimes, leading to a surge in liquidation events.
2. **H2 (Contrarian Positioning):** Accounts in the **Top 10% Decile** (cumulative net PnL) act counter-cyclically by accumulating Long positions during `Extreme Fear` and scaling Shorts during `Extreme Greed`.
3. **H3 (Win Rate Degradation):** Trader win rates exhibit significant variance across sentiment regimes ($H=13.78, p < 0.008$), with performance sharply dropping during rapid sentiment pivots.
4. **H4 (Volume Extremes):** Trading volume peaks at market sentiment boundaries (`Extreme Fear` and `Extreme Greed`), confirming extreme market sentiment as a high-volatility regime.

---

## Quickstart & Local Environment Setup

### 1. Requirements
* Python 3.10 or higher
* Recommended virtual environment: `python -m venv venv`

### 2. Installation
```bash
pip install pandas numpy matplotlib seaborn scipy reportlab fpdf2 jupyter
```

### 3. Execution Pipeline
1. **Data Processing & EDA:**
   ```bash
   python scratch/process_and_analyze.py
   ```
2. **Report Compilation:**
   ```bash
   python scratch/generate_report.py
   ```
3. **Jupyter Notebook Execution:**
   ```bash
   jupyter notebook notebook_1.ipynb
   ```

---

## License & Attribution
* **Trader Data:** Hyperliquid On-Chain Perpetual DEX Execution Logs
* **Sentiment Index:** Bitcoin Fear & Greed Index

