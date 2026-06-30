# Architecture

Market Entry Agent is organized as a small multi-agent system with a standardized data layer.

## Planner Agent

The Planner Agent receives `country`, `industry`, `product`, and optional `platform` input. It normalizes names, checks required fields, and emits a structured task object.

## Retriever Agent

The Retriever Agent reads `data/processed/market_entry_dataset.csv`. If the processed dataset does not exist, it automatically triggers `data_processing/build_dataset.py`.

It supports:

- country lookup
- industry lookup
- product lookup
- platform lookup
- combined country + industry + product lookup

It returns a context object containing model-ready metrics, source records, source URLs, missing fields, and data quality.

## Scoring Model

The Scoring Model calculates a 0-100 Market Entry Score using weighted dimensions:

- Market Demand: 30%
- Competition Intensity: 20%
- Ecommerce Readiness: 20%
- Pricing Potential: 15%
- Risk Level: 15%

## Demand Prediction Model

The Demand Prediction Model uses an interpretable rules-based index. It combines population, GDP per capita, ecommerce penetration, industry growth, review volume, rating, and price accessibility. It outputs demand level and estimated monthly sales range.

## Risk Model

The Risk Model evaluates:

- Market saturation risk
- Pricing pressure risk
- Regulatory risk
- Logistics risk
- Cultural fit risk

It outputs an overall risk level, numerical risk score, risk factors, and mitigation suggestions.

## Report Agent

The Report Agent converts context and model outputs into a Markdown market entry report with executive summary, market overview, product opportunity, competition analysis, demand prediction, scoring, risk assessment, and recommended entry strategy.

## Excel to Agent Workflow

Excel files are placed in `data/raw/`. `data_processing/build_dataset.py` reads every workbook and sheet, standardizes columns, preserves source metadata, appends sample fallback metrics, and exports:

- `data/processed/market_entry_dataset.csv`
- `data/processed/market_entry_dataset.json`
- `data/processed/market_entry_dataset.sqlite`

The Retriever Agent consumes these processed files during analysis.

