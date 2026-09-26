
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(
    page_title="EDA",
    page_icon="📈",
    layout="wide"
)

sns.set_theme(style="whitegrid")


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

st.title("📈 Exploratory Data Analysis")

st.write(
    "Select an analysis type to explore the data "
    "using different visualizations."
)

st.markdown("## 🔍 Select Analysis")

analysis_type = st.radio(
    "Choose Analysis",
    [
        "Univariate Analysis",
        "Bivariate Analysis",
        "Multivariate Analysis"
    ],
    horizontal=True
)


# ==================================================
# UNIVARIATE ANALYSIS
# ==================================================

if analysis_type == "Univariate Analysis":

    st.subheader("🔹 Univariate Analysis")

    st.write(
        "Univariate analysis examines one variable "
        "at a time."
    )

    choice = st.selectbox(
        "Choose a Plot",
        [
            "Sales Amount Distribution",
            "Units Sold Distribution",
            "Product Category Count",
            "Region Count"
        ]
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    if choice == "Sales Amount Distribution":

        sns.histplot(
            df["SalesAmount"],
            kde=True,
            ax=ax
        )

        ax.set_title(
            "Distribution of Sales Amount"
        )

        ax.set_xlabel("Sales Amount")

    elif choice == "Units Sold Distribution":

        sns.histplot(
            df["UnitsSold"],
            kde=True,
            ax=ax
        )

        ax.set_title(
            "Distribution of Units Sold"
        )

        ax.set_xlabel("Units Sold")

    elif choice == "Product Category Count":

        sns.countplot(
            data=df,
            x="ProductCategory",
            ax=ax
        )

        ax.set_title(
            "Product Category Frequency"
        )

        ax.tick_params(
            axis="x",
            rotation=25
        )

    else:

        sns.countplot(
            data=df,
            x="Region",
            ax=ax
        )

        ax.set_title("Region Frequency")

        ax.tick_params(
            axis="x",
            rotation=25
        )

    st.pyplot(fig)

    plt.close(fig)


# ==================================================
# BIVARIATE ANALYSIS
# ==================================================

elif analysis_type == "Bivariate Analysis":

    st.subheader("🔹 Bivariate Analysis")

    st.write(
        "Bivariate analysis examines the relationship "
        "between two variables."
    )

    choice = st.selectbox(
        "Choose a Plot",
        [
            "Sales by Product Category",
            "Sales by Region",
            "Units Sold vs Sales",
            "Sales by Payment Method"
        ]
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    if choice == "Sales by Product Category":

        data = (
            df.groupby("ProductCategory")
            ["SalesAmount"]
            .sum()
            .reset_index()
        )

        sns.barplot(
            data=data,
            x="ProductCategory",
            y="SalesAmount",
            ax=ax
        )

        ax.set_title(
            "Total Sales by Product Category"
        )

        ax.tick_params(
            axis="x",
            rotation=25
        )

    elif choice == "Sales by Region":

        data = (
            df.groupby("Region")
            ["SalesAmount"]
            .sum()
            .reset_index()
        )

        sns.barplot(
            data=data,
            x="Region",
            y="SalesAmount",
            ax=ax
        )

        ax.set_title("Total Sales by Region")

        ax.tick_params(
            axis="x",
            rotation=25
        )

    elif choice == "Units Sold vs Sales":

        sns.scatterplot(
            data=df,
            x="UnitsSold",
            y="SalesAmount",
            hue="ProductCategory",
            ax=ax
        )

        ax.set_title(
            "Units Sold vs Sales Amount"
        )

    else:

        data = (
            df.groupby("PaymentMethod")
            ["SalesAmount"]
            .sum()
            .reset_index()
        )

        sns.barplot(
            data=data,
            x="PaymentMethod",
            y="SalesAmount",
            ax=ax
        )

        ax.set_title(
            "Total Sales by Payment Method"
        )

        ax.tick_params(
            axis="x",
            rotation=25
        )

    st.pyplot(fig)

    plt.close(fig)


# ==================================================
# MULTIVARIATE ANALYSIS
# ==================================================

else:

    st.subheader("🔹 Multivariate Analysis")

    st.write(
        "Multivariate analysis examines three or "
        "more variables together."
    )

    choice = st.selectbox(
        "Choose a Plot",
        [
            "Correlation Heatmap",
            "Sales by Region and Category",
            "Sales, Units and Category"
        ]
    )

    if choice == "Correlation Heatmap":

        numeric_df = df[
            [
                "SalesAmount",
                "UnitsSold",
                "DeliveryDays"
            ]
        ].corr()

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        sns.heatmap(
            numeric_df,
            annot=True,
            cmap="coolwarm",
            fmt=".2f",
            ax=ax
        )

        ax.set_title(
            "Correlation Heatmap"
        )

        st.pyplot(fig)

        plt.close(fig)

    elif choice == "Sales by Region and Category":

        pivot = pd.pivot_table(
            df,
            values="SalesAmount",
            index="Region",
            columns="ProductCategory",
            aggfunc="sum",
            fill_value=0
        )

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        sns.heatmap(
            pivot,
            annot=True,
            fmt=".0f",
            cmap="YlGnBu",
            ax=ax
        )

        ax.set_title(
            "Sales by Region and Product Category"
        )

        st.pyplot(fig)

        plt.close(fig)

    else:

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        sns.scatterplot(
            data=df,
            x="UnitsSold",
            y="SalesAmount",
            size="DeliveryDays",
            hue="Region",
            style="ProductCategory",
            sizes=(30, 250),
            ax=ax
        )

        ax.set_title(
            "Sales, Units, Delivery Days and Category"
        )

        st.pyplot(fig)

        plt.close(fig)


st.markdown("---")

st.caption(
    "Charts created using NumPy, Pandas, "
    "Seaborn and Matplotlib."
)