
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.set_page_config(
    page_title="Conclusions",
    page_icon="✅",
    layout="wide"
)


@st.cache_data
def load_data():
    file_path = (
        Path(__file__).resolve().parent.parent
        / "Indian_Market_Sales (1).csv"
    )

    df = pd.read_csv(file_path)

    df["OrderDate"] = pd.to_datetime(
        df["OrderDate"], errors="coerce"
    )

    df["DeliveryDate"] = pd.to_datetime(
        df["DeliveryDate"], errors="coerce"
    )

    df["DeliveryDays"] = (
        df["DeliveryDate"] - df["OrderDate"]
    ).dt.days

    return df


df = load_data()

st.title("✅ Conclusions & Key Findings")

st.write(
    "This page provides a summary of the "
    "sales dataset."
)

total_sales = np.sum(
    df["SalesAmount"]
)

total_units = np.sum(
    df["UnitsSold"]
)

average_sale = np.mean(
    df["SalesAmount"]
)

average_units = np.mean(
    df["UnitsSold"]
)

top_category = (
    df.groupby("ProductCategory")
    ["SalesAmount"]
    .sum()
    .idxmax()
)

top_region = (
    df.groupby("Region")
    ["SalesAmount"]
    .sum()
    .idxmax()
)

top_payment = (
    df.groupby("PaymentMethod")
    ["SalesAmount"]
    .sum()
    .idxmax()
)

average_delivery = np.mean(
    df["DeliveryDays"]
)

st.markdown("## 📊 Summary Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Sales",
    f"₹{total_sales:,.0f}"
)

col2.metric(
    "Average Sale",
    f"₹{average_sale:,.0f}"
)

col3.metric(
    "Average Units Sold",
    f"{average_units:,.2f}"
)

st.markdown("## 🔍 Main Observations")

st.info(
    f"Top Product Category by Sales: {top_category}"
)

st.info(
    f"Top Region by Sales: {top_region}"
)

st.info(
    f"Most Used Payment Method by Sales: {top_payment}"
)

st.info(
    f"Average Delivery Duration: "
    f"{average_delivery:,.2f} days"
)

st.markdown("## 📌 Conclusion")

st.write("""
The analysis helps identify sales patterns across
categories, regions, and payment methods.

EDA plots can be used to explore distributions,
relationships, and correlations.

These findings can support further business
analysis and decision-making.
""")

st.markdown("## 🚀 Suggestions for Further Analysis")

st.write("""
- Compare monthly sales trends.
- Analyze holiday versus non-holiday sales.
- Study delivery duration by region.
- Investigate the relationship between units sold
  and sales amount.
- Build a predictive model for future sales.
""")