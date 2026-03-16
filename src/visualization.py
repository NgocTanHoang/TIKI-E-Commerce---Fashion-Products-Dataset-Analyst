"""
Visualization module for Tiki product data analysis.
Provides reusable plotting functions for EDA and business insights.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from config import MAIN_CATEGORIES

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def plot_price_distributions_by_category(df, category_col='main_category', price_col='price'):
    """
    Plot price distributions across categories.

    Args:
        df (pd.DataFrame): Input dataframe
        category_col (str): Category column
        price_col (str): Price column
    """
    plt.figure(figsize=(12, 6))
    for category in df[category_col].unique():
        subset = df[df[category_col] == category]
        sns.kdeplot(data=subset, x=price_col, label=category, fill=True, alpha=0.3)

    plt.title('Price Distributions by Category')
    plt.xlabel('Price (VND)')
    plt.ylabel('Density')
    plt.legend()
    plt.xlim(0, df[price_col].quantile(0.95))  # Focus on main distribution
    plt.show()

def plot_rating_heatmaps(df, category_col='main_category', rating_col='rating_average', review_col='review_count'):
    """
    Plot rating heatmaps showing average rating vs review count by category.

    Args:
        df (pd.DataFrame): Input dataframe
        category_col (str): Category column
        rating_col (str): Rating column
        review_col (str): Review count column
    """
    # Create pivot table
    pivot = df.pivot_table(
        values=rating_col,
        index=category_col,
        columns=pd.cut(df[review_col], bins=5),
        aggfunc='mean'
    )

    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, cmap='YlGnBu', fmt='.2f')
    plt.title('Average Rating by Category and Review Count Bins')
    plt.xlabel('Review Count Bins')
    plt.ylabel('Category')
    plt.show()

def plot_inventory_vs_performance(df, x_col='quantity_sold', y_col='rating_average',
                                size_col='favourite_count', category_col='main_category'):
    """
    Scatter plot of inventory (sales) vs performance metrics.

    Args:
        df (pd.DataFrame): Input dataframe
        x_col (str): X-axis column (inventory/sales)
        y_col (str): Y-axis column (performance)
        size_col (str): Size column for bubble size
        category_col (str): Category column for coloring
    """
    plt.figure(figsize=(12, 8))

    # Sample for better visualization if too many points
    if len(df) > 1000:
        df_plot = df.sample(1000, random_state=42)
    else:
        df_plot = df

    scatter = plt.scatter(
        df_plot[x_col],
        df_plot[y_col],
        s=df_plot[size_col] / df_plot[size_col].max() * 200 + 20,  # Scale bubble size
        c=pd.Categorical(df_plot[category_col]).codes,
        cmap='tab10',
        alpha=0.6,
        edgecolors='black',
        linewidth=0.5
    )

    plt.title('Inventory vs Performance (Bubble size = Favourite Count)')
    plt.xlabel(x_col.replace('_', ' ').title())
    plt.ylabel(y_col.replace('_', ' ').title())
    plt.colorbar(scatter, label=category_col.replace('_', ' ').title())

    # Add trend line
    z = np.polyfit(df_plot[x_col], df_plot[y_col], 1)
    p = np.poly1d(z)
    plt.plot(df_plot[x_col], p(df_plot[x_col]), "r--", alpha=0.8)

    plt.show()

def plot_sales_trends_over_time(df, date_col='date_created', sales_col='quantity_sold',
                               category_col='main_category'):
    """
    Plot sales trends over time by category.

    Args:
        df (pd.DataFrame): Input dataframe
        date_col (str): Date column
        sales_col (str): Sales column
        category_col (str): Category column
    """
    if date_col not in df.columns:
        print(f"Warning: {date_col} not found, skipping time trend plot")
        return

    # Group by month and category
    df_time = df.copy()
    df_time['month'] = pd.to_datetime(df_time[date_col]).dt.to_period('M')

    monthly_sales = df_time.groupby(['month', category_col])[sales_col].sum().reset_index()
    monthly_sales['month'] = monthly_sales['month'].dt.to_timestamp()

    plt.figure(figsize=(14, 8))
    sns.lineplot(data=monthly_sales, x='month', y=sales_col, hue=category_col, marker='o')

    plt.title('Sales Trends Over Time by Category')
    plt.xlabel('Date')
    plt.ylabel('Total Sales Volume')
    plt.xticks(rotation=45)
    plt.legend(title=category_col.replace('_', ' ').title())
    plt.show()

def plot_fulfillment_impact(df, fulfillment_col='fulfillment_type', metric_col='rating_average'):
    """
    Plot impact of fulfillment type on performance metrics.

    Args:
        df (pd.DataFrame): Input dataframe
        fulfillment_col (str): Fulfillment type column
        metric_col (str): Performance metric column
    """
    plt.figure(figsize=(10, 6))

    # Box plot
    sns.boxplot(data=df, x=fulfillment_col, y=metric_col)
    plt.title(f'{metric_col.replace("_", " ").title()} by Fulfillment Type')
    plt.xlabel('Fulfillment Type')
    plt.ylabel(metric_col.replace('_', ' ').title())
    plt.show()

    # Bar plot of counts
    plt.figure(figsize=(8, 5))
    fulfillment_counts = df[fulfillment_col].value_counts()
    fulfillment_counts.plot(kind='bar')
    plt.title('Distribution of Fulfillment Types')
    plt.xlabel('Fulfillment Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.show()

def plot_correlation_matrix(df, numeric_cols=None):
    """
    Plot correlation matrix for numeric columns.

    Args:
        df (pd.DataFrame): Input dataframe
        numeric_cols (list): List of numeric columns to include
    """
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    corr_matrix = df[numeric_cols].corr()

    plt.figure(figsize=(12, 10))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm', center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    plt.title('Correlation Matrix of Numeric Features')
    plt.show()

def plot_category_performance(df, category_col='main_category', metrics=['rating_average', 'quantity_sold', 'price'], show=True):
    """
    Plot performance metrics by category.

    Args:
        df (pd.DataFrame): Input dataframe
        category_col (str): Category column
        metrics (list): List of metrics to plot
    """
    fig, axes = plt.subplots(1, len(metrics), figsize=(5*len(metrics), 6))

    for i, metric in enumerate(metrics):
        ax = axes[i] if len(metrics) > 1 else axes
        category_stats = df.groupby(category_col)[metric].agg(['mean', 'std', 'count'])
        category_stats['mean'].plot(kind='bar', yerr=category_stats['std'], ax=ax, capsize=5)
        ax.set_title(f'Average {metric.replace("_", " ").title()} by Category')
        ax.set_xlabel('Category')
        ax.set_ylabel(metric.replace('_', ' ').title())
        ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()

def create_eda_report(df):
    """
    Generate a comprehensive EDA visualization report.

    Args:
        df (pd.DataFrame): Input dataframe
    """
    print("Generating EDA Visualization Report...")

    # Price distributions
    plot_price_distributions_by_category(df)

    # Rating heatmaps
    plot_rating_heatmaps(df)

    # Inventory vs performance
    plot_inventory_vs_performance(df)

    # Correlation matrix
    numeric_cols = ['price', 'original_price', 'rating_average', 'review_count',
                   'favourite_count', 'quantity_sold', 'discount_pct', 'composite_score']
    available_cols = [col for col in numeric_cols if col in df.columns]
    plot_correlation_matrix(df, available_cols)

    # Category performance
    plot_category_performance(df)

    # Fulfillment impact
    if 'fulfillment_type' in df.columns:
        plot_fulfillment_impact(df)

    # Time trends if date available
    if 'date_created' in df.columns:
        plot_sales_trends_over_time(df)

    print("EDA report generation complete.")