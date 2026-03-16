"""
Metrics module for calculating key performance indicators (KPIs).
Contains formulas for business metrics and performance calculations.
"""

import pandas as pd
import numpy as np

def calculate_roi(revenue, cost):
    """
    Calculate Return on Investment (ROI).

    Args:
        revenue (float or pd.Series): Revenue amount
        cost (float or pd.Series): Cost amount

    Returns:
        float or pd.Series: ROI percentage
    """
    return ((revenue - cost) / cost) * 100

def calculate_conversion_rate(sales, visitors):
    """
    Calculate conversion rate (estimated).

    Args:
        sales (int): Number of sales
        visitors (int): Number of visitors (estimated from reviews)

    Returns:
        float: Conversion rate percentage
    """
    if visitors == 0:
        return 0
    return (sales / visitors) * 100

def calculate_customer_satisfaction_score(rating, review_count, max_reviews=1000):
    """
    Calculate customer satisfaction score combining rating and review volume.

    Args:
        rating (float): Average rating (0-5)
        review_count (int): Number of reviews
        max_reviews (int): Maximum review count for normalization

    Returns:
        float: Satisfaction score (0-100)
    """
    # Normalize rating to 0-50
    rating_score = (rating / 5) * 50

    # Normalize review count to 0-50 (more reviews = more confidence)
    review_score = min(review_count / max_reviews, 1) * 50

    return rating_score + review_score

def calculate_inventory_turnover(sales, avg_inventory_value, time_period=30):
    """
    Calculate inventory turnover ratio.

    Args:
        sales (float): Sales amount
        avg_inventory_value (float): Average inventory value
        time_period (int): Time period in days

    Returns:
        float: Turnover ratio
    """
    if avg_inventory_value == 0:
        return 0
    return (sales * (365 / time_period)) / avg_inventory_value

def calculate_gross_margin(revenue, cogs):
    """
    Calculate gross margin percentage.

    Args:
        revenue (float): Total revenue
        cogs (float): Cost of goods sold

    Returns:
        float: Gross margin percentage
    """
    if revenue == 0:
        return 0
    return ((revenue - cogs) / revenue) * 100

def calculate_abc_classification_value(total_value, cumulative_pct):
    """
    Classify product into ABC category based on cumulative percentage.

    Args:
        total_value (float): Product's total value
        cumulative_pct (float): Cumulative percentage of total value

    Returns:
        str: ABC category ('A', 'B', or 'C')
    """
    if cumulative_pct <= 80:
        return 'A'
    elif cumulative_pct <= 95:
        return 'B'
    else:
        return 'C'

def calculate_pareto_ratio(top_20pct_items, total_items):
    """
    Calculate Pareto ratio (80/20 rule adherence).

    Args:
        top_20pct_items (int): Number of items making 80% of value
        total_items (int): Total number of items

    Returns:
        float: Pareto ratio (lower is better adherence to 80/20)
    """
    return top_20pct_items / total_items

def calculate_discount_impact(discount_pct, sales_before, sales_after):
    """
    Calculate the impact of discount on sales.

    Args:
        discount_pct (float): Discount percentage
        sales_before (float): Sales before discount
        sales_after (float): Sales after discount

    Returns:
        dict: Impact metrics
    """
    sales_increase = sales_after - sales_before
    sales_increase_pct = (sales_increase / sales_before) * 100 if sales_before > 0 else 0

    return {
        'sales_increase': sales_increase,
        'sales_increase_pct': sales_increase_pct,
        'profit_impact': sales_increase * (1 - discount_pct)  # Simplified
    }

def calculate_seasonal_index(values, period=12):
    """
    Calculate seasonal index for time series data.

    Args:
        values (pd.Series): Time series values
        period (int): Seasonal period (e.g., 12 for monthly)

    Returns:
        pd.Series: Seasonal indices
    """
    if len(values) < period:
        return pd.Series([1.0] * len(values), index=values.index)

    # Calculate seasonal averages
    seasonal_avg = values.groupby(values.index % period).mean()

    # Calculate overall average
    overall_avg = values.mean()

    # Calculate seasonal indices
    seasonal_indices = seasonal_avg / overall_avg

    return seasonal_indices

def calculate_price_elasticity(price_change_pct, quantity_change_pct):
    """
    Calculate price elasticity of demand.

    Args:
        price_change_pct (float): Percentage change in price
        quantity_change_pct (float): Percentage change in quantity

    Returns:
        float: Price elasticity
    """
    if price_change_pct == 0:
        return 0
    return quantity_change_pct / price_change_pct

def calculate_market_share(category_sales, total_market_sales):
    """
    Calculate market share percentage.

    Args:
        category_sales (float): Sales of the category
        total_market_sales (float): Total market sales

    Returns:
        float: Market share percentage
    """
    if total_market_sales == 0:
        return 0
    return (category_sales / total_market_sales) * 100