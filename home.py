
import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Indian Market Sales",
    page_icon="📊",
    layout="wide"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():

    file_path = (
        Path(__file__).resolve().parent
        / "Indian_Market_Sales (1).csv"
    )

    df = pd.read_csv(file_path)

    df["OrderDate"] = pd.to_datetime(
        df["OrderDate"],
        errors="coerce"
    )

    df["DeliveryDate"] = pd.to_datetime(
        df["DeliveryDate"],
        errors="coerce"
    )

    df["DeliveryDays"] = (
        df["DeliveryDate"] - df["OrderDate"]
    ).dt.days

    return df


# ==================================================
# LOAD DATA SAFELY
# ==================================================

try:

    df = load_data()

except FileNotFoundError:

    st.error(
        "CSV file not found. "
        "Please check the file name and folder location."
    )

    st.stop()


# ==================================================
# SIDEBAR NAVIGATION
# ==================================================

st.sidebar.title("📊 Indian Market Sales")

page = st.sidebar.radio(
    "Select a Page",
    [
        "🏠 Home",
        "📋 Introduction",
        "📈 EDA",
        "✅ Conclusion"
    ]
)


# ==================================================
# HOME DASHBOARD
# ==================================================

if page == "🏠 Home":

    st.title("🇮🇳 Indian Market Sales Dashboard")

    st.subheader(
        "Explore sales performance through data analysis"
    )

    st.write(
        "This dashboard uses Pandas, NumPy, "
        "Seaborn, and Matplotlib."
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


# ==================================================
# INTRODUCTION PAGE
# ==================================================

elif page == "📋 Introduction":

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
            df[col].nunique()
            for col in df.columns
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


# ==================================================
# EDA PAGE
# ==================================================

elif page == "📈 EDA":

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


    # ==============================================
    # UNIVARIATE ANALYSIS
    # ==============================================

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


    # ==============================================
    # BIVARIATE ANALYSIS
    # ==============================================

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


    # ==============================================
    # MULTIVARIATE ANALYSIS
    # ==============================================

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


# ==================================================
# CONCLUSION PAGE
# ==================================================

elif page == "✅ Conclusion":

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


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "Charts created using NumPy, Pandas, "
    "Seaborn and Matplotlib."
)