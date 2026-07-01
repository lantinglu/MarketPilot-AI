"""Streamlit app for the Market Entry Agent portfolio demo."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from config import STANDARD_DATASET_CSV
from main import run_market_entry_analysis


REQUIRED_METRICS = {
    "gdp_per_capita",
    "population",
    "ecommerce_penetration",
    "industry_growth_rate",
    "average_price",
    "average_rating",
    "review_volume",
    "competition_level",
    "regulatory_complexity",
    "logistics_complexity",
    "cultural_fit_score",
}

DEMO_SCENARIOS = {
    "US Beauty": {
        "country": "United States",
        "industry": "Beauty",
        "product": "Mineral Sunscreen Stick",
    },
    "Japan Home": {
        "country": "Japan",
        "industry": "Home & Kitchen",
        "product": "Smart Insulated Lunch Box",
    },
    "Germany Electronics": {
        "country": "Germany",
        "industry": "Consumer Electronics",
        "product": "Bluetooth Sleep Earbuds",
    },
    "Vietnam Sports": {
        "country": "Vietnam",
        "industry": "Sports & Outdoors",
        "product": "Adjustable Resistance Bands",
    },
}


@st.cache_data
def load_scenario_options() -> pd.DataFrame:
    dataset = pd.read_csv(STANDARD_DATASET_CSV)
    metric_rows = dataset[dataset["metric_name"].isin(REQUIRED_METRICS)].copy()
    metric_rows = metric_rows.dropna(subset=["country", "industry", "product"])
    coverage = (
        metric_rows.groupby(["country", "industry", "product", "platform"], dropna=False)["metric_name"]
        .nunique()
        .reset_index(name="metric_count")
    )
    coverage = coverage[coverage["metric_count"] >= len(REQUIRED_METRICS)]
    return coverage.sort_values(["country", "industry", "product", "platform"]).reset_index(drop=True)


def options_for(df: pd.DataFrame, column: str) -> list[str]:
    return sorted(value for value in df[column].dropna().astype(str).unique() if value)


def index_for(options: list[str], selected: str) -> int:
    return options.index(selected) if selected in options else 0


def apply_demo_scenario(name: str) -> None:
    scenario = DEMO_SCENARIOS[name]
    st.session_state.selected_country = scenario["country"]
    st.session_state.selected_industry = scenario["industry"]
    st.session_state.product_input = scenario["product"]
    st.session_state.auto_generate = True


def ensure_state(scenarios: pd.DataFrame) -> None:
    countries = options_for(scenarios, "country")
    if "selected_country" not in st.session_state:
        st.session_state.selected_country = "United States" if "United States" in countries else countries[0]

    country_rows = scenarios[scenarios["country"] == st.session_state.selected_country]
    industries = options_for(country_rows, "industry")
    if "selected_industry" not in st.session_state or st.session_state.selected_industry not in industries:
        st.session_state.selected_industry = "Beauty" if "Beauty" in industries else industries[0]

    industry_rows = country_rows[country_rows["industry"] == st.session_state.selected_industry]
    products = options_for(industry_rows, "product")
    if "product_input" not in st.session_state:
        st.session_state.product_input = products[0] if products else ""


def platform_options(scenarios: pd.DataFrame, country: str, industry: str) -> list[str]:
    rows = scenarios[(scenarios["country"] == country) & (scenarios["industry"] == industry)]
    return options_for(rows, "platform")


def scenario_count_label(scenarios: pd.DataFrame) -> str:
    countries = scenarios["country"].nunique()
    industries = scenarios["industry"].nunique()
    scenario_count = scenarios.groupby(["country", "industry", "product", "platform"]).ngroups
    return f"{countries} markets · {industries} industries · {scenario_count} benchmark scenarios"


st.set_page_config(page_title="Market Entry Agent", layout="wide")

scenarios = load_scenario_options()

if scenarios.empty:
    st.error("No model-ready scenarios found in the processed dataset. Please rebuild the dataset first.")
    st.stop()

ensure_state(scenarios)

st.title("Cross-border Market Entry Report Generator")
st.caption("跨境市场进入报告生成器 · Select a market, choose an industry, enter any product, and generate a bilingual market-entry report.")

with st.sidebar:
    st.header("Scenario Builder")
    st.caption(scenario_count_label(scenarios))

    st.markdown("**Quick demos**")
    demo_cols = st.columns(2)
    for idx, name in enumerate(DEMO_SCENARIOS):
        with demo_cols[idx % 2]:
            if st.button(name, use_container_width=True):
                apply_demo_scenario(name)
                st.rerun()

    st.divider()

    countries = options_for(scenarios, "country")
    country = st.selectbox(
        "Market / 国家",
        countries,
        index=index_for(countries, st.session_state.selected_country),
        key="selected_country",
    )

    country_rows = scenarios[scenarios["country"] == country]
    industries = options_for(country_rows, "industry")
    industry = st.selectbox(
        "Industry / 行业",
        industries,
        index=index_for(industries, st.session_state.selected_industry),
        key="selected_industry",
    )

    industry_rows = country_rows[country_rows["industry"] == industry]
    example_products = options_for(industry_rows, "product")
    default_product = example_products[0] if example_products else ""
    if not st.session_state.get("product_input"):
        st.session_state.product_input = default_product

    product = st.text_input(
        "Product / 产品",
        key="product_input",
        help="Enter any product. If product-level data is unavailable, the agent uses country + industry benchmark metrics.",
    )

    platforms = platform_options(scenarios, country, industry)
    platform = st.selectbox("Platform / 平台", platforms) if platforms else ""

    generate = st.button("Generate Report", type="primary", use_container_width=True)

should_generate = generate or st.session_state.pop("auto_generate", False)

if should_generate:
    try:
        with st.spinner("Generating bilingual market-entry report..."):
            result = run_market_entry_analysis(country, industry, product, platform)
        st.session_state.latest_result = result
    except Exception as exc:
        st.error(f"报告生成失败 / Failed to generate report: {exc}")

result = st.session_state.get("latest_result")

if result:
    chinese_report, english_report = result["report"].split("\n\n---\n\n", maxsplit=1)
    task = result["task"]
    data_quality = result["context"]["data_quality"]

    st.subheader("Executive Snapshot / 执行摘要")
    score_col, demand_col, risk_col, sales_col = st.columns(4)
    score_col.metric("Market Entry Score", f"{result['score']['total_score']}/100")
    demand_col.metric("Demand", result["demand"]["predicted_demand_level"])
    risk_col.metric("Risk", result["risk"]["overall_risk"])
    sales_col.metric("Monthly Sales", result["demand"]["estimated_monthly_sales_range"])

    st.success(result["recommendation"])

    if data_quality == "industry_benchmark":
        st.warning("Product-level data is not available. This report uses benchmark metrics for the selected country and industry.")
    elif data_quality == "benchmark_estimate":
        st.info("This report uses benchmark estimate data for demo screening and scenario comparison.")

    action_cols = st.columns([1, 1, 2])
    with action_cols[0]:
        st.download_button(
            "Download Markdown",
            data=result["report"],
            file_name=f"market_entry_report_{task['country']}_{task['industry']}_{task['product']}.md".replace(" ", "_"),
            mime="text/markdown",
            use_container_width=True,
        )
    with action_cols[1]:
        st.download_button(
            "Download Chinese",
            data=chinese_report,
            file_name=f"cn_report_{task['country']}_{task['product']}.md".replace(" ", "_"),
            mime="text/markdown",
            use_container_width=True,
        )

    report_tab, english_tab, score_tab, data_tab = st.tabs(["中文报告", "English Report", "Score Breakdown", "Data"])
    with report_tab:
        st.markdown(chinese_report)
    with english_tab:
        st.markdown(english_report)
    with score_tab:
        st.dataframe(
            pd.DataFrame(
                [
                    {"Dimension": key, "Score": value}
                    for key, value in result["score"]["dimension_scores"].items()
                ]
            ),
            use_container_width=True,
            hide_index=True,
        )
        st.markdown("**Risk factors**")
        st.write(result["risk"]["risk_factors"])
        st.markdown("**Mitigation suggestions**")
        st.write(result["risk"]["mitigation_suggestions"])
    with data_tab:
        st.write("Scenario", result["task"])
        st.write("Metrics", result["context"]["metrics"])
        st.write("Demand", result["demand"])
        st.write("Data quality", data_quality)
        st.caption("Demo data combines structured source rows, benchmark estimates, and transparent rule-based scoring. Validate with live marketplace data before client decisions.")
else:
    intro_col, flow_col = st.columns([1.2, 1])
    with intro_col:
        st.subheader("Generate a client-ready market entry report")
        st.write(
            "Pick a target market and industry, enter any product name, then generate a bilingual report with score, demand forecast, risk assessment, and recommended entry strategy."
        )
        st.info("Use the quick demo buttons in the sidebar for a fast presentation flow.")
    with flow_col:
        st.subheader("Demo story")
        st.markdown(
            """
1. A seller wants to launch a product overseas.
2. The agent combines market, industry, platform, and benchmark data.
3. It returns a bilingual report for early screening and client discussion.
"""
        )
