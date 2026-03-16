"""
Simple dashboard for Tiki product analysis using Streamlit.
Run with: streamlit run src/dashboard.py
"""

import streamlit as st
import pandas as pd
import sys
import os

# Add src to path
sys.path.append('../src')

from preprocessing import preprocess_data
from performance_analysis import generate_performance_report
from inventory_analysis import generate_inventory_report
from visualization import plot_price_distributions_by_category
from utils import format_currency

# Page configuration
st.set_page_config(
    page_title="Tiki Product Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Tiki E-commerce Product Analysis Dashboard")
st.markdown("Business Performance & Inventory Management Insights")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Choose Analysis", [
    "Overview",
    "Performance Analysis",
    "Inventory Management",
    "Category Insights"
])

# Load data (cached)
@st.cache_data
def load_data():
    return preprocess_data()

@st.cache_data
def load_reports():
    df = load_data()
    perf_report, df_perf = generate_performance_report(df)
    inv_report, df_inv = generate_inventory_report(df)
    return df, perf_report, inv_report

# Load data
with st.spinner("Loading data..."):
    df, perf_report, inv_report = load_reports()

# Main content
if page == "Overview":
    st.header("📈 Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Products", f"{inv_report['total_products']:,}")

    with col2:
        st.metric("Categories", len(df['main_category'].unique()))

    with col3:
        st.metric("Brands", len(df['brand'].dropna().unique()))

    with col4:
        st.metric("Sellers", len(df['current_seller'].unique()))

    # Key metrics
    st.subheader("Key Performance Indicators")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Average Performance Score", f"{perf_report['avg_performance_score']:.3f}")
        st.metric("Top Category", perf_report['top_category'])

    with col2:
        st.metric("Inventory Turnover Rate", f"{inv_report['avg_turnover_rate']:.2f} units/day")
        st.metric("ABC A Products", f"{inv_report['abc_distribution'].get('A', 0):,}")

elif page == "Performance Analysis":
    st.header("🎯 Performance Analysis")

    # Pareto Analysis
    st.subheader("Pareto Principle (80/20 Rule)")
    pareto_data = []
    for cat, data in perf_report['pareto_analysis'].items():
        pareto_data.append({
            'Category': cat,
            'Pareto Ratio': data['pareto_ratio'],
            'Products for 80% Value': data['products_for_80pct_value']
        })

    pareto_df = pd.DataFrame(pareto_data)
    st.dataframe(pareto_df)

    # Top Products
    st.subheader("Top Performing Products")
    top_products = pd.DataFrame(perf_report['top_performing_products'])
    st.dataframe(top_products)

    # Discount Effectiveness
    st.subheader("Discount Effectiveness")
    discount_corr = perf_report['discount_effectiveness']['correlations']
    st.write(f"Discount vs Sales Correlation: {discount_corr.get('discount_pct', {}).get('quantity_sold', 0):.3f}")

elif page == "Inventory Management":
    st.header("📦 Inventory Management")

    # ABC Analysis
    st.subheader("ABC Classification")
    abc_data = inv_report['abc_distribution']
    st.bar_chart(pd.Series(abc_data))

    # Stock-out Risk
    st.subheader("Stock-out Risk Distribution")
    risk_data = inv_report['stockout_risk_distribution']
    if risk_data:
        st.bar_chart(pd.Series(risk_data))

    # SKU Rationalization
    st.subheader("SKU Rationalization Opportunities")
    sku_data = inv_report['sku_rationalization']
    st.metric("SKUs to Review", sku_data['total_skus_to_review'])

    st.write("High-risk categories:")
    for cat in sku_data['high_risk_categories']:
        st.write(f"- {cat}")

elif page == "Category Insights":
    st.header("📊 Category Insights")

    # Category selection
    categories = df['main_category'].unique()
    selected_category = st.selectbox("Select Category", categories)

    # Category data
    cat_data = df[df['main_category'] == selected_category]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Products", len(cat_data))

    with col2:
        st.metric("Avg Price", format_currency(cat_data['price'].mean()))

    with col3:
        st.metric("Avg Rating", f"{cat_data['rating_average'].mean():.2f}")

    # Price distribution
    st.subheader("Price Distribution")
    fig, ax = plt.subplots()
    cat_data['price'].hist(bins=30, ax=ax)
    ax.set_xlabel('Price (VND)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("*Dashboard generated from Tiki product analysis pipeline*")