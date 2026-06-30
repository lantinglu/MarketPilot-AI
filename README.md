# Market Entry Agent

An AI-powered multi-agent system that helps businesses evaluate whether a product should enter a target overseas market.

This project is designed as an AI Agent competition MVP and portfolio-ready GitHub repository. It combines a planner agent, structured data retrieval, scoring logic, demand prediction, risk modeling, and Markdown report generation into a runnable market entry analysis workflow.

## Project Overview

Market Entry Agent answers a practical business question:

> Given a country, industry, and product, should this product enter the target market?

The system takes user input, retrieves relevant country, industry, product, platform, and source data, calculates a Market Entry Score, predicts demand, evaluates risks, and generates a complete market entry report.

## Demo Input

```text
Country: Japan
Industry: Home & Kitchen
Product: Vacuum Flask
```

Additional supported sample inputs:

```text
Country: United States
Industry: Beauty
Product: Sunscreen
```

```text
Country: Germany
Industry: Consumer Electronics
Product: Wireless Earbuds
```

## Demo Output

```text
Market Entry Score: 61.6/100
Demand Level: High
Estimated Monthly Sales: 5,921 - 10,855 units
Overall Risk: Medium
Recommendation: Enter cautiously after validation tests
```

The full report is generated at:

```text
outputs/sample_report.md
```

## Agent Workflow

1. User enters `country + industry + product`.
2. Planner Agent standardizes input and creates a task object.
3. Retriever Agent searches the processed dataset and returns structured context.
4. Risk Model evaluates business and market-entry risk.
5. Scoring Model calculates a weighted 0-100 Market Entry Score.
6. Demand Prediction Model estimates demand level and monthly sales range.
7. Report Agent generates a Markdown market entry report.

## Dataset Description

The project supports Excel-based source ingestion. Raw Excel files are placed in:

```text
data/raw/
```

The data processing pipeline reads every workbook and sheet, standardizes fields, preserves source metadata, and exports:

```text
data/processed/market_entry_dataset.csv
data/processed/market_entry_dataset.json
data/processed/market_entry_dataset.sqlite
```

Canonical schema:

```text
country
industry
product
platform
metric_name
metric_value
metric_unit
source_name
source_url
source_type
updated_date
notes
```

If Excel data is incomplete, the pipeline appends a sample dataset so the project remains independently runnable.

## Tech Stack

- Python
- pandas
- openpyxl
- SQLite
- Streamlit
- pytest
- Markdown reports
- Mermaid documentation diagrams

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Build the processed dataset from Excel and sample records:

```bash
python data_processing/build_dataset.py
```

Run the command-line demo:

```bash
python main.py
```

Run the Streamlit app:

```bash
streamlit run app.py
```

Run tests:

```bash
pytest
```

## Example Report

The generated report includes:

- Executive Summary
- Market Overview
- Product Opportunity
- Competition Analysis
- Demand Prediction
- Market Entry Score
- Risk Assessment
- Recommended Entry Strategy
- Data Quality Note

See `docs/sample_output.md` and `outputs/sample_report.md`.

## Future Improvements

- Integrate live marketplace APIs such as Amazon, Rakuten, Walmart, Shopee, Lazada, and eBay.
- Add Google Trends and social media listening signals.
- Pull macroeconomic indicators from World Bank, IMF, OECD, and national statistics APIs.
- Replace the rules-based demand model with trained sklearn, XGBoost, or time-series models.
- Add LLM-based report writing, analyst critique, and reasoning trace generation.
- Introduce multi-agent orchestration with planner, retriever, analyst, critic, and report writer agents.
- Add PDF export, scenario comparison, and historical run storage.
- Add authentication and deploy the Streamlit app to a public demo environment.

## Why This Project Matters

International market entry decisions require combining fragmented signals: macro data, ecommerce readiness, platform availability, competitive pressure, product reviews, pricing, and regulatory risk. This project demonstrates how an AI Agent system can transform those signals into a structured, explainable decision workflow.

For AI Agent competitions and interviews, the project shows:

- practical agent decomposition
- structured data ingestion from Excel
- graceful handling of missing data
- interpretable scoring and prediction models
- reproducible outputs
- a usable UI and command-line demo
- documentation suitable for a real GitHub repository

