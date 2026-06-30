"""Streamlit app for the Market Entry Agent portfolio demo."""

from __future__ import annotations

import streamlit as st

from main import run_market_entry_analysis


st.set_page_config(page_title="Market Entry Agent", layout="wide")

st.title("Market Entry Agent")
st.caption("AI-powered multi-agent market entry analysis for overseas product launches.")

with st.sidebar:
    st.header("Input")
    country = st.text_input("Country", value="Japan")
    industry = st.text_input("Industry", value="Home & Kitchen")
    product = st.text_input("Product", value="Vacuum Flask")
    platform = st.text_input("Platform (optional)", value="")
    run_button = st.button("Generate Report", type="primary")

if run_button:
    try:
        result = run_market_entry_analysis(country, industry, product, platform)
        score_col, demand_col, risk_col, rec_col = st.columns(4)
        score_col.metric("Market Entry Score", f"{result['score']['total_score']}/100")
        demand_col.metric("Demand", result["demand"]["predicted_demand_level"])
        risk_col.metric("Risk", result["risk"]["overall_risk"])
        rec_col.metric("Data Quality", result["context"]["data_quality"])

        st.subheader("Final Recommendation")
        st.success(result["recommendation"])

        st.subheader("Demand Prediction")
        st.write(result["demand"])

        st.subheader("Risk Assessment")
        st.write(result["risk"])

        st.subheader("Markdown Report")
        st.markdown(result["report"])
    except Exception as exc:
        st.error(f"Failed to generate report: {exc}")
else:
    st.info("Enter a country, industry, and product, then click Generate Report.")
