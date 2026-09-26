
import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Indian Market Sales",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    file_path = (
        Path(__file__).resolve().parent
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

st.sidebar.title("📊 Indian Market Sales")
st.sidebar.info(
    "Select a page from the sidebar."
)

st.title("🇮🇳 Indian Market Sales Dashboard")

st.subheader(
    "Explore sales performance through data analysis"
)

st.write(
    "This dashboard uses Pandas, NumPy, Seaborn, "
    "and Matplotlib for analysis."
)

st.success("Dataset loaded successfully!")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"₹{np.sum(df['SalesAmount']):,.0f}"
)

col2.metric(
    "Total Units",
    f"{np.sum(df['UnitsSold']):,.0f}"
)

col3.metric(
    "Total Orders",
    f"{df['SaleID'].nunique():,.0f}"
)

col4.metric(
    "Regions",
    f"{df['Region'].nunique():,.0f}"
)

st.markdown("### 📋 Data Preview")

st.dataframe(
    df.head(10),
    use_container_width=True
)