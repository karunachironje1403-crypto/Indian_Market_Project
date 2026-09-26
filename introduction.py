
import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Introduction",
    page_icon="🏠",
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

st.title("🏠 Introduction & Data Information")

st.write(
    "This page provides an overview of the "
    "Indian Market Sales dataset."
)

st.markdown("## 🎯 Project Objective")

st.write("""
The objective of this project is to analyze sales
performance across product categories, regions,
payment methods, and delivery durations.
""")

st.markdown("## 📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])

col3.metric(
    "Missing Values",
    int(df.isna().sum().sum())
)

col4.metric(
    "Categories",
    df["ProductCategory"].nunique()
)

st.markdown("## 🧾 Column Information")

info = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str).values,
    "Missing Values": df.isna().sum().values,
    "Unique Values": [
        df[col].nunique() for col in df.columns
    ]
})

st.dataframe(
    info,
    use_container_width=True
)

st.markdown("## 👀 Data Preview")

st.dataframe(
    df,
    use_container_width=True
)

st.markdown("## 📈 Statistical Summary")

st.dataframe(
    df.describe(include="all").transpose(),
    use_container_width=True
)