# Product Requirements Document (PRD)
## Web3 Trading Team – Trader Behavior & Market Sentiment Analysis

---

## 1. Executive Summary & Overview

### 1.1 Project Title
**Web3 Trading Analytics: Hyperliquid Trader Behavior vs. Bitcoin Market Sentiment Analysis**

### 1.2 Objective & Scope
The objective of this project is to conduct a comprehensive data science investigation into the relationship between decentralised exchange (Hyperliquid) trader behavior and macro Bitcoin market sentiment (Fear & Greed Index). By joining high-frequency trade execution logs with market sentiment metrics, the analysis aims to uncover actionable trading insights, behavioral biases, risk patterns, and predictive strategy signals.

### 1.3 Key Problem Statement
How do trading performance, leverage usage, position directional bias (Long vs. Short), and trade volumes vary across market sentiment regimes (Extreme Fear, Fear, Neutral, Greed, Extreme Greed)? Do top-performing traders align with or trade counter-cyclically to broad market sentiment?

---

## 2. Dataset Specifications

### 2.1 Bitcoin Market Sentiment Dataset (Fear & Greed Index)
* **Source URL:** [Google Drive - Fear & Greed Dataset](https://drive.google.com/file/d/1PgQC0tO8XN-wqkNyghWc_-mnrYv_nhSf/view?usp=sharing)
* **Core Columns:**
  * `Date` (`YYYY-MM-DD` or timestamp): Date of recorded sentiment score.
  * `Classification` (Categorical): Sentiment label (`Extreme Fear`, `Fear`, `Neutral`, `Greed`, `Extreme Greed`).
  * *(Optional/Derived Score)* `Value` (Numeric 0-100): Numerical representation of the sentiment index.

### 2.2 Historical Trader Data (Hyperliquid On-Chain Perpetual DEX)
* **Source URL:** [Google Drive - Historical Trader Data](https://drive.google.com/file/d/1IAfLZwu6rJzyWKgBToqwSmmVYU6VbjVs/view?usp=sharing)
* **Core Columns:**
  * `account` (String): Unique wallet address or account identifier.
  * `symbol` (String): Traded asset contract (e.g., `BTC`, `ETH`, `SOL`).
  * `execution price` (Float): Price at which trade order executed.
  * `size` (Float): Trade order magnitude / quantity.
  * `side` (Categorical): Direction of the execution (`Buy`, `Sell`, `Long`, `Short`).
  * `time` (Timestamp): Execution Unix timestamp / ISO datetime.
  * `start position` (Float): Open position size before trade execution.
  * `event` (String): Type of event (`Open`, `Close`, `Liquidation`, `Fill`, etc.).
  * `closedPnL` (Float): Realized profit and loss upon closing position.
  * `leverage` (Float): Margin multiplier applied to the position.

---

## 3. Core Hypotheses & Analytical Pillars

### 3.1 Hypothesis Framework
1. **H1 (Leverage Escalation):** Retail/underperforming traders utilize significantly higher leverage during `Extreme Greed` regimes compared to `Extreme Fear` regimes.
2. **H2 (Contrarian Profitability):** Accounts with top-decile cumulative `closedPnL` exhibit contrarian positioning (initiating Longs during `Extreme Fear` and Shorts during `Extreme Greed`).
3. **H3 (Win Rate vs. Sentiment):** Average trader win rates deteriorate during sentiment transitions (e.g., pivot from Greed to Fear) due to delayed adaptation.
4. **H4 (Volume & Activity Spikes):** Trading activity and liquidation frequency peak at sentiment extremes (`Extreme Greed` and `Extreme Fear`).

### 3.2 Analytical Pillars
* **Pillar 1: Data Alignment & Cleaning:** Time-zone standardization (UTC), deduplication, missing value imputation, daily aggregation of trade metrics.
* **Pillar 2: Sentiment-Driven Behavior Segmentation:** Metric breakdowns (PnL, volume, leverage, long/short ratio) across sentiment categories.
* **Pillar 3: Cohort & Leaderboard Analysis:** Profiling top 10% vs bottom 10% traders by PnL across market regimes.
* **Pillar 4: Statistical & Correlation Analysis:** Correlation matrix between Fear/Greed values and aggregate market volume, average leverage, net PnL.
* **Pillar 5: Strategy Insights & Recommendations:** Formulating actionable signals for Web3 algorithmic execution based on empirical findings.

---

## 4. Deliverables & Standardized Submission Requirements

All candidates must strictly adhere to the directory and artifact layout outlined below. Non-compliance results in automatic rejection.

### 4.1 Root Directory Naming
```bash
ds_<candidate_name>/
```

### 4.2 Required Directory & File Structure
```
ds_<candidate_name>/
├── notebook_1.ipynb      # Main Google Colab Notebook (Data Preprocessing, Merging, Core EDA)
├── notebook_2.ipynb      # (Optional) Secondary Notebook (Advanced Modeling / Strategy Backtesting)
├── csv_files/            # Directory containing processed datasets and aggregated metrics
│   ├── merged_trader_sentiment.csv
│   ├── daily_sentiment_metrics.csv
│   └── trader_cohort_summary.csv
├── outputs/              # High-resolution charts, plots, and figures
│   ├── pnl_vs_sentiment.png
│   ├── leverage_distribution_by_regime.png
│   ├── long_short_ratio_heatmap.png
│   └── winrate_by_cohort.png
├── ds_report.pdf         # Final executive presentation & detailed findings report
└── README.md             # Setup guide, execution order, Colab links, and summary
```

### 4.3 Technical Execution Standards
* **Environment:** All code must run natively in Google Colab.
* **Sharing Permissions:** Colab links must be set to `Anyone with the link can view`.
* **Version Control:** Repository must be hosted on GitHub with identical folder structure.

---

## 5. Implementation Roadmap & Milestones

| Milestone | Task Description | Key Output / Artifact |
| :--- | :--- | :--- |
| **Phase 1** | Download & inspect datasets from Google Drive links | Raw data inspection logs |
| **Phase 2** | Preprocess, clean timestamps, aggregate Hyperliquid trade logs | Cleaned Dataframes in `csv_files/` |
| **Phase 3** | Merge trade metrics with Fear & Greed daily classification | `merged_trader_sentiment.csv` |
| **Phase 4** | Exploratory Data Analysis & Visualizations | Generated PNG graphs in `outputs/` |
| **Phase 5** | Hypotheses validation & statistical testing | Section in `notebook_1.ipynb` |
| **Phase 6** | Executive report compilation | `ds_report.pdf` |
| **Phase 7** | Repository packaging & Colab links verification | `README.md` & GitHub repo push |

---

## 6. Verification & Quality Evaluation Criteria

1. **Rigor of Analysis:** Proper handling of trade execution data, leverage, and realized PnL.
2. **Visual Communication:** Clean, publication-ready charts in `outputs/` with legible axes and clear legend keys.
3. **Reproducibility:** Self-contained Jupyter notebooks with structured markdown headers and runnable code blocks.
4. **Actionable Insights:** Concrete recommendations for Web3 trading strategies based on trader behavior during market extremes.
