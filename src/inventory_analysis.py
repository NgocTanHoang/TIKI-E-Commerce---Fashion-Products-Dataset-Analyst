"""
Inventory analysis module for Tiki product data.
Provides functions for inventory health assessment and recommendations.
"""

import pandas as pd
import numpy as np
from .config import METRIC_THRESHOLDS

def calculate_stock_turnover(df, sales_col='quantity_sold', price_col='price',
                           time_period_days=30):
    """
    Calculate inventory turnover ratio.
    Turnover = (Sales Volume * Average Price) / (Average Inventory Value * Time Period)

    Since we don't have current inventory value, we'll use sales as proxy.

    Args:
        df (pd.DataFrame): Input dataframe
        sales_col (str): Sales volume column
        price_col (str): Price column
        time_period_days (int): Time period for turnover calculation

    Returns:
        pd.DataFrame: Dataframe with turnover metrics
    """
    df = df.copy()

    # Calculate sales value
    df['sales_value'] = df[sales_col] * df[price_col]

    # Turnover rate (simplified: sales per day)
    df['turnover_rate'] = df[sales_col] / time_period_days

    # Turnover ratio (sales value / estimated inventory value)
    # Using sales value as proxy for inventory value
    df['turnover_ratio'] = df['sales_value'] / (df['sales_value'].mean())  # Normalized

    print(f"Calculated inventory turnover metrics for {len(df)} products")
    return df

def identify_slow_movers(df, sales_col='quantity_sold', threshold=None):
    """
    Identify slow-moving inventory items.

    Args:
        df (pd.DataFrame): Input dataframe
        sales_col (str): Sales column
        threshold (float): Sales threshold below which items are slow movers

    Returns:
        pd.DataFrame: Dataframe with slow mover flags
    """
    if threshold is None:
        threshold = METRIC_THRESHOLDS.get('low_stock_threshold', 10)

    df = df.copy()
    df['is_slow_mover'] = df[sales_col] < threshold

    slow_movers = df[df['is_slow_mover']]
    print(f"Identified {len(slow_movers)} slow-moving products ({len(slow_movers)/len(df)*100:.1f}%)")

    return df

def identify_fast_movers(df, sales_col='quantity_sold', threshold=None):
    """
    Identify fast-moving inventory items.

    Args:
        df (pd.DataFrame): Input dataframe
        sales_col (str): Sales column
        threshold (float): Sales threshold above which items are fast movers

    Returns:
        pd.DataFrame: Dataframe with fast mover flags
    """
    if threshold is None:
        threshold = METRIC_THRESHOLDS.get('top_seller_threshold', 1000)

    df = df.copy()
    df['is_fast_mover'] = df[sales_col] > threshold

    fast_movers = df[df['is_fast_mover']]
    print(f"Identified {len(fast_movers)} fast-moving products ({len(fast_movers)/len(df)*100:.1f}%)")

    return df

def recommend_restock_priorities(df, sales_col='quantity_sold', rating_col='rating_average',
                               review_col='review_count', category_col='main_category'):
    """
    Generate restock priority recommendations based on sales velocity and performance.

    Args:
        df (pd.DataFrame): Input dataframe
        sales_col (str): Sales column
        rating_col (str): Rating column
        review_col (str): Review count column
        category_col (str): Category column

    Returns:
        pd.DataFrame: Dataframe with restock priorities
    """
    df = df.copy()

    # Calculate priority score
    # Higher score = higher restock priority
    df['restock_priority'] = (
        (df[sales_col] / df[sales_col].max()) * 0.4 +  # Sales velocity
        (df[rating_col] / 5.0) * 0.3 +  # Rating quality
        (df[review_col] / df[review_col].max()) * 0.3  # Review volume
    )

    # Rank within categories
    df['category_rank'] = df.groupby(category_col)['restock_priority'].rank(ascending=False)

    # Priority levels
    df['priority_level'] = pd.cut(
        df['restock_priority'],
        bins=[0, 0.3, 0.7, 1.0],
        labels=['Low', 'Medium', 'High']
    )

    print("Generated restock priority recommendations")
    return df

def calculate_inventory_health_score(df, sales_col='quantity_sold', rating_col='rating_average',
                                   stock_threshold=10, rating_threshold=4.0):
    """
    Calculate overall inventory health score for each product.

    Args:
        df (pd.DataFrame): Input dataframe
        sales_col (str): Sales column
        rating_col (str): Rating column
        stock_threshold (float): Minimum stock threshold
        rating_threshold (float): Minimum rating threshold

    Returns:
        pd.DataFrame: Dataframe with health scores
    """
    df = df.copy()

    # Stock health (0-1 scale)
    df['stock_health'] = np.clip(df[sales_col] / stock_threshold, 0, 1)

    # Rating health (0-1 scale)
    df['rating_health'] = df[rating_col] / 5.0

    # Combined health score
    df['inventory_health_score'] = (df['stock_health'] * 0.6 + df['rating_health'] * 0.4)

    # Health categories
    df['health_category'] = pd.cut(
        df['inventory_health_score'],
        bins=[0, 0.3, 0.7, 1.0],
        labels=['Poor', 'Fair', 'Good']
    )

    print("Calculated inventory health scores")
    return df

def analyze_inventory_by_category(df, category_col='main_category', sales_col='quantity_sold'):
    """
    Analyze inventory metrics aggregated by category.

    Args:
        df (pd.DataFrame): Input dataframe
        category_col (str): Category column
        sales_col (str): Sales column

    Returns:
        pd.DataFrame: Category-level inventory analysis
    """
    category_analysis = df.groupby(category_col).agg({
        sales_col: ['sum', 'mean', 'std', 'count'],
        'price': ['mean', 'min', 'max'],
        'rating_average': 'mean',
        'is_slow_mover': 'sum',
        'is_fast_mover': 'sum'
    }).round(2)

    # Flatten column names
    category_analysis.columns = ['_'.join(col).strip() for col in category_analysis.columns.values]

    # Calculate percentages
    category_analysis['slow_mover_pct'] = (
        category_analysis['is_slow_mover_sum'] / category_analysis[f'{sales_col}_count'] * 100
    ).round(1)

    category_analysis['fast_mover_pct'] = (
        category_analysis['is_fast_mover_sum'] / category_analysis[f'{sales_col}_count'] * 100
    ).round(1)

    print("Completed category-level inventory analysis")
    return category_analysis

def forecast_demand_simple(df, sales_col='quantity_sold', periods=30):
    """
    Simple demand forecasting using moving averages.

    Args:
        df (pd.DataFrame): Input dataframe
        sales_col (str): Sales column
        periods (int): Forecast periods

    Returns:
        pd.DataFrame: Dataframe with demand forecasts
    """
    df = df.copy()

    # Simple exponential smoothing forecast
    alpha = 0.3  # Smoothing factor
    df['demand_forecast'] = df[sales_col].ewm(alpha=alpha).mean()

    # Forecast next periods (simplified)
    last_value = df['demand_forecast'].iloc[-1]
    df['forecast_next_period'] = last_value * (1 + (df[sales_col].pct_change().mean()))

    print(f"Generated simple demand forecasts for {periods} periods")
    return df

def perform_abc_analysis(df, value_col='quantity_sold', price_col='price'):
    """
    Perform ABC analysis for inventory classification.
    Classifies products into A, B, C categories based on cumulative value contribution.

    Args:
        df (pd.DataFrame): Input dataframe
        value_col (str): Column for value calculation (sales volume)
        price_col (str): Price column for revenue calculation

    Returns:
        pd.DataFrame: Dataframe with ABC classifications
    """
    df = df.copy()

    # Calculate total value (revenue proxy: price * sales)
    df['total_value'] = df[price_col] * df[value_col]

    # Sort by total value descending
    df = df.sort_values(by='total_value', ascending=False)

    # Calculate cumulative percentage
    total_value = df['total_value'].sum()
    df['cumulative_value'] = df['total_value'].cumsum()
    df['cumulative_pct'] = (df['cumulative_value'] / total_value) * 100

    # Classify ABC
    def classify_abc(percentage):
        if percentage <= 80:
            return 'A'  # High value, tight control
        elif percentage <= 95:
            return 'B'  # Medium value, moderate control
        else:
            return 'C'  # Low value, minimal control

    df['abc_category'] = df['cumulative_pct'].apply(classify_abc)

    abc_counts = df['abc_category'].value_counts()
    print(f"ABC Analysis completed: A={abc_counts.get('A', 0)}, B={abc_counts.get('B', 0)}, C={abc_counts.get('C', 0)} products")

    return df

def estimate_stockout_risk(df, sales_col='quantity_sold', date_col='date_created',
                          current_stock_col=None):
    """
    Estimate stock-out risk based on sales velocity and time data.

    Args:
        df (pd.DataFrame): Input dataframe
        sales_col (str): Sales column
        date_col (str): Date column for time-based analysis
        current_stock_col (str): Current stock column (if available)

    Returns:
        pd.DataFrame: Dataframe with stock-out risk estimates
    """
    df = df.copy()

    if date_col in df.columns:
        # Calculate days since creation
        df['days_since_creation'] = (pd.Timestamp.now() - pd.to_datetime(df[date_col])).dt.days

        # Calculate daily sales rate (run-rate)
        df['daily_sales_rate'] = df[sales_col] / df['days_since_creation'].clip(lower=1)

        # Estimate stock-out risk (higher rate = higher risk if no current stock data)
        try:
            df['stockout_risk'] = pd.cut(
                df['daily_sales_rate'],
                bins=[-np.inf, df['daily_sales_rate'].quantile(0.33),
                      df['daily_sales_rate'].quantile(0.67), np.inf],
                labels=['Low', 'Medium', 'High'],
                duplicates='drop'
            )
        except ValueError:
            # Fallback if quantiles are not unique
            df['stockout_risk'] = pd.cut(
                df['daily_sales_rate'],
                bins=3,
                labels=['Low', 'Medium', 'High'],
                duplicates='drop'
            )

        # Estimate days until stock-out (if we assume current stock = sales)
        if current_stock_col is None:
            df['estimated_days_to_stockout'] = df[sales_col] / df['daily_sales_rate'].clip(lower=0.1)
        else:
            df['estimated_days_to_stockout'] = df[current_stock_col] / df['daily_sales_rate'].clip(lower=0.1)

        print("Stock-out risk estimation completed using time-based analysis")
    else:
        # Fallback: use sales volume as risk proxy
        df['stockout_risk'] = pd.cut(
            df[sales_col],
            bins=[0, df[sales_col].quantile(0.33),
                  df[sales_col].quantile(0.67), df[sales_col].max()],
            labels=['Low', 'Medium', 'High']
        )
        print("Stock-out risk estimation completed using sales volume proxy")

    return df

def analyze_sku_rationalization(df, category_col='main_category', sales_col='quantity_sold',
                               threshold_pct=10):
    """
    Analyze SKU rationalization opportunities.
    Identifies categories with too many low-performing products.

    Args:
        df (pd.DataFrame): Input dataframe
        category_col (str): Category column
        sales_col (str): Sales column
        threshold_pct (float): Percentage threshold for low performers

    Returns:
        dict: SKU rationalization recommendations
    """
    results = {}

    for category in df[category_col].unique():
        category_df = df[df[category_col] == category]

        total_products = len(category_df)
        threshold_value = category_df[sales_col].quantile(threshold_pct / 100)
        low_performers = category_df[category_df[sales_col] <= threshold_value]

        results[category] = {
            'total_skus': total_products,
            'low_performing_skus': len(low_performers),
            'low_performer_pct': len(low_performers) / total_products * 100,
            'rationalization_opportunity': len(low_performers) > total_products * 0.3,  # >30% low performers
            'avg_sales_top_10pct': category_df[category_df[sales_col] > category_df[sales_col].quantile(0.9)][sales_col].mean(),
            'avg_sales_bottom_10pct': low_performers[sales_col].mean()
        }

    # Overall recommendations
    high_risk_categories = [cat for cat, data in results.items() if data['rationalization_opportunity']]

    recommendations = {
        'category_analysis': results,
        'high_risk_categories': high_risk_categories,
        'total_skus_to_review': sum(data['low_performing_skus'] for data in results.values()),
        'recommendations': [
            f"Review {len(high_risk_categories)} categories with high low-performer ratios",
            "Consider SKU reduction for products with sales below category threshold",
            "Focus on top 10% performers for inventory optimization"
        ]
    }

    print(f"SKU rationalization analysis completed for {len(results)} categories")
    return recommendations

def generate_inventory_report(df):
    """
    Generate comprehensive inventory analysis report.

    Args:
        df (pd.DataFrame): Input dataframe

    Returns:
        dict: Report with key findings
    """
    # Apply all inventory analyses
    df = calculate_stock_turnover(df)
    df = identify_slow_movers(df)
    df = identify_fast_movers(df)
    df = recommend_restock_priorities(df)
    df = calculate_inventory_health_score(df)

    # New advanced analyses
    df = perform_abc_analysis(df)
    df = estimate_stockout_risk(df)
    sku_analysis = analyze_sku_rationalization(df)

    # Category analysis
    category_report = analyze_inventory_by_category(df)

    # Summary statistics
    report = {
        'total_products': len(df),
        'slow_movers_count': df['is_slow_mover'].sum(),
        'fast_movers_count': df['is_fast_mover'].sum(),
        'avg_turnover_rate': df['turnover_rate'].mean(),
        'top_category_by_sales': category_report['quantity_sold_sum'].idxmax(),
        'health_distribution': df['health_category'].value_counts().to_dict(),
        'abc_distribution': df['abc_category'].value_counts().to_dict(),
        'stockout_risk_distribution': df['stockout_risk'].value_counts().to_dict() if 'stockout_risk' in df.columns else {},
        'category_analysis': category_report.to_dict(),
        'sku_rationalization': sku_analysis
    }

    print("Generated comprehensive inventory analysis report")
    return report, df