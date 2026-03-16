"""
Performance analysis module for Tiki product data.
Provides functions for product scoring, ranking, and performance insights.
"""

import pandas as pd
import numpy as np
from .config import METRIC_THRESHOLDS

def calculate_product_score(df, weights=None):
    """
    Calculate composite performance score for products.

    Args:
        df (pd.DataFrame): Input dataframe
        weights (dict): Weights for different metrics

    Returns:
        pd.DataFrame: Dataframe with performance scores
    """
    if weights is None:
        weights = {
            'rating_average': 0.3,
            'review_count': 0.25,
            'favourite_count': 0.2,
            'quantity_sold': 0.15,
            'discount_pct': 0.1
        }

    df = df.copy()

    # Normalize metrics to 0-1 scale
    df['rating_norm'] = df['rating_average'] / 5.0
    df['review_norm'] = df['review_count'] / df['review_count'].max()
    df['favourite_norm'] = df['favourite_count'] / df['favourite_count'].max()
    df['sales_norm'] = df['quantity_sold'] / df['quantity_sold'].max()
    df['discount_norm'] = df['discount_pct']  # Already 0-1

    # Calculate weighted score
    df['performance_score'] = (
        df['rating_norm'] * weights['rating_average'] +
        df['review_norm'] * weights['review_count'] +
        df['favourite_norm'] * weights['favourite_count'] +
        df['sales_norm'] * weights['quantity_sold'] +
        df['discount_norm'] * weights['discount_pct']
    )

    print(f"Calculated performance scores for {len(df)} products")
    return df

def rank_products_by_performance(df, score_col='performance_score', top_n=10):
    """
    Rank products by performance score.

    Args:
        df (pd.DataFrame): Input dataframe
        score_col (str): Performance score column
        top_n (int): Number of top products to return

    Returns:
        pd.DataFrame: Top performing products
    """
    if score_col not in df.columns:
        df = calculate_product_score(df)

    top_products = df.nlargest(top_n, score_col)[
        ['id', 'name', score_col, 'rating_average', 'review_count',
         'quantity_sold', 'price', 'main_category']
    ]

    print(f"Top {top_n} performing products identified")
    return top_products

def identify_top_sellers(df, sales_col='quantity_sold', threshold=None):
    """
    Identify top-selling products.

    Args:
        df (pd.DataFrame): Input dataframe
        sales_col (str): Sales column
        threshold (float): Sales threshold for top sellers

    Returns:
        pd.DataFrame: Top selling products
    """
    if threshold is None:
        threshold = METRIC_THRESHOLDS.get('top_seller_threshold', 1000)

    top_sellers = df[df[sales_col] >= threshold].copy()
    top_sellers = top_sellers.sort_values(sales_col, ascending=False)

    print(f"Identified {len(top_sellers)} top-selling products")
    return top_sellers

def analyze_brand_performance(df, brand_col='brand', metrics=['rating_average', 'quantity_sold', 'price']):
    """
    Analyze performance metrics by brand.

    Args:
        df (pd.DataFrame): Input dataframe
        brand_col (str): Brand column
        metrics (list): Metrics to analyze

    Returns:
        pd.DataFrame: Brand performance analysis
    """
    brand_analysis = df.groupby(brand_col).agg({
        'rating_average': ['mean', 'std', 'count'],
        'quantity_sold': ['sum', 'mean'],
        'price': ['mean', 'min', 'max'],
        'review_count': 'sum'
    }).round(2)

    # Flatten column names
    brand_analysis.columns = ['_'.join(col).strip() for col in brand_analysis.columns.values]

    # Filter brands with minimum products
    min_products = 5
    brand_analysis = brand_analysis[brand_analysis['rating_average_count'] >= min_products]

    # Sort by average rating
    brand_analysis = brand_analysis.sort_values('rating_average_mean', ascending=False)

    print(f"Analyzed performance for {len(brand_analysis)} brands")
    return brand_analysis

def analyze_category_trends(df, category_col='main_category',
                          metrics=['rating_average', 'quantity_sold', 'price']):
    """
    Analyze performance trends by category.

    Args:
        df (pd.DataFrame): Input dataframe
        category_col (str): Category column
        metrics (list): Metrics to analyze

    Returns:
        pd.DataFrame: Category performance analysis
    """
    category_analysis = df.groupby(category_col).agg({
        'rating_average': ['mean', 'std', 'min', 'max'],
        'quantity_sold': ['sum', 'mean', 'std'],
        'price': ['mean', 'std', 'min', 'max'],
        'review_count': ['sum', 'mean'],
        'favourite_count': ['sum', 'mean'],
        'discount_pct': 'mean'
    }).round(2)

    # Flatten column names
    category_analysis.columns = ['_'.join(col).strip() for col in category_analysis.columns.values]

    # Add market share calculation
    total_sales = category_analysis['quantity_sold_sum'].sum()
    category_analysis['market_share_pct'] = (
        category_analysis['quantity_sold_sum'] / total_sales * 100
    ).round(1)

    # Sort by total sales
    category_analysis = category_analysis.sort_values('quantity_sold_sum', ascending=False)

    print(f"Analyzed trends for {len(category_analysis)} categories")
    return category_analysis

def analyze_seller_performance(df, seller_col='current_seller'):
    """
    Analyze performance by seller.

    Args:
        df (pd.DataFrame): Input dataframe
        seller_col (str): Seller column

    Returns:
        pd.DataFrame: Seller performance analysis
    """
    seller_analysis = df.groupby(seller_col).agg({
        'id': 'count',  # Number of products
        'rating_average': 'mean',
        'quantity_sold': 'sum',
        'price': 'mean',
        'review_count': 'sum'
    }).round(2)

    seller_analysis = seller_analysis.rename(columns={'id': 'product_count'})

    # Filter sellers with minimum products
    seller_analysis = seller_analysis[seller_analysis['product_count'] >= 3]

    # Calculate seller score
    seller_analysis['seller_score'] = (
        (seller_analysis['rating_average'] / 5.0) * 0.4 +
        (seller_analysis['quantity_sold'] / seller_analysis['quantity_sold'].max()) * 0.4 +
        (seller_analysis['product_count'] / seller_analysis['product_count'].max()) * 0.2
    )

    # Sort by seller score
    seller_analysis = seller_analysis.sort_values('seller_score', ascending=False)

    print(f"Analyzed performance for {len(seller_analysis)} sellers")
    return seller_analysis

def identify_performance_outliers(df, score_col='performance_score', threshold=2.0):
    """
    Identify products that are performance outliers.

    Args:
        df (pd.DataFrame): Input dataframe
        score_col (str): Performance score column
        threshold (float): Z-score threshold for outliers

    Returns:
        pd.DataFrame: Outlier products
    """
    if score_col not in df.columns:
        df = calculate_product_score(df)

    # Calculate z-scores
    df['score_zscore'] = (df[score_col] - df[score_col].mean()) / df[score_col].std()

    # Identify outliers
    outliers = df[abs(df['score_zscore']) > threshold].copy()
    outliers = outliers.sort_values('score_zscore', ascending=False)

    print(f"Identified {len(outliers)} performance outliers")
    return outliers

def calculate_roi_estimate(df, sales_col='quantity_sold', price_col='price',
                          cost_pct=0.6):  # Assume 60% cost of goods
    """
    Estimate ROI for products (simplified calculation).

    Args:
        df (pd.DataFrame): Input dataframe
        sales_col (str): Sales column
        price_col (str): Price column
        cost_pct (float): Estimated cost percentage

    Returns:
        pd.DataFrame: Dataframe with ROI estimates
    """
    df = df.copy()

    # Estimated revenue
    df['estimated_revenue'] = df[sales_col] * df[price_col]

    # Estimated cost (simplified)
    df['estimated_cost'] = df['estimated_revenue'] * cost_pct

    # Estimated profit
    df['estimated_profit'] = df['estimated_revenue'] - df['estimated_cost']

    # ROI (Return on Investment)
    df['estimated_roi'] = df['estimated_profit'] / df['estimated_cost']

    print("Calculated ROI estimates for products")
    return df

def analyze_pareto_principle(df, value_col='quantity_sold', category_col='main_category'):
    """
    Analyze Pareto principle (80/20 rule) for products within each category.
    Identifies top 20% products that generate 80% of value.

    Args:
        df (pd.DataFrame): Input dataframe
        value_col (str): Column to use for value calculation (sales, revenue, etc.)
        category_col (str): Category column for analysis

    Returns:
        dict: Pareto analysis results by category
    """
    results = {}

    for category in df[category_col].unique():
        category_df = df[df[category_col] == category].copy()
        category_df = category_df.sort_values(value_col, ascending=False)

        total_value = category_df[value_col].sum()
        category_df['cumulative_value'] = category_df[value_col].cumsum()
        category_df['cumulative_pct'] = (category_df['cumulative_value'] / total_value) * 100

        # Find products that make up 80% of value
        top_80_pct_products = category_df[category_df['cumulative_pct'] <= 80]
        top_20_pct_count = int(len(category_df) * 0.2)

        results[category] = {
            'total_products': len(category_df),
            'top_20pct_products': top_20_pct_count,
            'products_for_80pct_value': len(top_80_pct_products),
            'pareto_ratio': len(top_80_pct_products) / len(category_df),
            'top_products': top_80_pct_products.head(5)[['id', value_col, 'cumulative_pct']].to_dict('records')
        }

    print(f"Pareto analysis completed for {len(results)} categories")
    return results

def analyze_discount_effectiveness(df, discount_col='discount_pct', sales_col='quantity_sold',
                                 rating_col='rating_average', review_col='review_count'):
    """
    Analyze the effectiveness of discounts on sales and customer engagement.

    Args:
        df (pd.DataFrame): Input dataframe
        discount_col (str): Discount percentage column
        sales_col (str): Sales volume column
        rating_col (str): Rating column
        review_col (str): Review count column

    Returns:
        dict: Discount effectiveness analysis
    """
    # Create discount bins
    df = df.copy()
    df['discount_bucket'] = pd.cut(df[discount_col],
                                   bins=[0, 0.1, 0.2, 0.3, 0.5, 1.0],
                                   labels=['0-10%', '10-20%', '20-30%', '30-50%', '50%+'])

    # Analyze by discount bucket
    discount_analysis = df.groupby('discount_bucket').agg({
        sales_col: ['mean', 'sum', 'count'],
        rating_col: 'mean',
        review_col: 'mean',
        discount_col: 'mean'
    }).round(3)

    # Flatten columns
    discount_analysis.columns = ['_'.join(col).strip() for col in discount_analysis.columns.values]

    # Correlation analysis
    correlation_matrix = df[[discount_col, sales_col, rating_col, review_col]].corr()

    results = {
        'discount_buckets': discount_analysis.to_dict(),
        'correlations': correlation_matrix.to_dict(),
        'key_insights': {
            'discount_sales_corr': correlation_matrix.loc[discount_col, sales_col],
            'discount_rating_corr': correlation_matrix.loc[discount_col, rating_col],
            'high_discount_products': len(df[df[discount_col] > 0.3]),
            'no_discount_products': len(df[df[discount_col] == 0])
        }
    }

    print("Discount effectiveness analysis completed")
    return results

def analyze_brand_equity(df, brand_col='brand', sales_col='quantity_sold',
                        rating_col='rating_average', price_col='price'):
    """
    Compare performance between branded and no-brand products.

    Args:
        df (pd.DataFrame): Input dataframe
        brand_col (str): Brand column
        sales_col (str): Sales column
        rating_col (str): Rating column
        price_col (str): Price column

    Returns:
        dict: Brand equity analysis
    """
    df = df.copy()

    # Classify branded vs no-brand
    df['brand_type'] = df[brand_col].apply(lambda x: 'Branded' if pd.notna(x) and str(x).strip() != '' else 'No-brand')

    # Analysis by brand type
    brand_analysis = df.groupby('brand_type').agg({
        sales_col: ['mean', 'sum', 'std'],
        rating_col: ['mean', 'std'],
        price_col: ['mean', 'std'],
        'id': 'count'
    }).round(2)

    # Flatten columns
    brand_analysis.columns = ['_'.join(col).strip() for col in brand_analysis.columns.values]

    # Top brands analysis
    top_brands = df[df['brand_type'] == 'Branded'].groupby(brand_col).agg({
        sales_col: 'sum',
        rating_col: 'mean',
        'id': 'count'
    }).sort_values(sales_col, ascending=False).head(10)

    # Calculate brand premium safely
    brand_premium = {}
    if 'Branded' in brand_analysis.index and 'No-brand' in brand_analysis.index:
        brand_premium = {
            'price_difference': brand_analysis.loc['Branded', f'{price_col}_mean'] - brand_analysis.loc['No-brand', f'{price_col}_mean'],
            'rating_difference': brand_analysis.loc['Branded', f'{rating_col}_mean'] - brand_analysis.loc['No-brand', f'{rating_col}_mean'],
            'sales_difference': brand_analysis.loc['Branded', f'{sales_col}_mean'] - brand_analysis.loc['No-brand', f'{sales_col}_mean']
        }
    else:
        brand_premium = {
            'price_difference': 0,
            'rating_difference': 0,
            'sales_difference': 0,
            'note': 'Insufficient data for brand comparison'
        }

    results = {
        'brand_vs_nobrand': brand_analysis.to_dict(),
        'top_brands': top_brands.to_dict(),
        'brand_premium': brand_premium
    }

    print("Brand equity analysis completed")
    return results

def generate_performance_report(df):
    """
    Generate comprehensive performance analysis report.

    Args:
        df (pd.DataFrame): Input dataframe

    Returns:
        dict: Report with key findings
    """
    # Apply performance analyses
    df = calculate_product_score(df)

    top_products = rank_products_by_performance(df, top_n=10)
    top_sellers = identify_top_sellers(df)
    brand_analysis = analyze_brand_performance(df)
    category_analysis = analyze_category_trends(df)
    seller_analysis = analyze_seller_performance(df)
    outliers = identify_performance_outliers(df)

    # New advanced analyses
    pareto_analysis = analyze_pareto_principle(df)
    discount_analysis = analyze_discount_effectiveness(df)
    brand_equity = analyze_brand_equity(df)

    # Summary statistics
    report = {
        'total_products': len(df),
        'avg_performance_score': df['performance_score'].mean(),
        'top_performing_products': top_products.to_dict('records'),
        'top_sellers_count': len(top_sellers),
        'top_brand': brand_analysis.index[0] if not brand_analysis.empty else None,
        'top_category': category_analysis.index[0] if not category_analysis.empty else None,
        'performance_outliers_count': len(outliers),
        'category_analysis': category_analysis.to_dict(),
        'brand_analysis': brand_analysis.head(5).to_dict(),
        'pareto_analysis': pareto_analysis,
        'discount_effectiveness': discount_analysis,
        'brand_equity': brand_equity
    }

    print("Generated comprehensive performance analysis report")
    return report, df