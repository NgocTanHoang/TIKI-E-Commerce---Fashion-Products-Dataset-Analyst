"""
Visualization module for Tiki product data analysis.
Provides reusable plotting functions for EDA and business insights.
Enhanced with interactive Plotly charts and improved label handling.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .config import MAIN_CATEGORIES

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def _add_mean_median_lines(ax, data, orientation='vertical', color='red', linestyle='--', alpha=0.7):
    """
    Add mean and median reference lines to a plot.

    Args:
        ax: Matplotlib axis object
        data: Data to calculate mean/median from
        orientation: 'vertical' or 'horizontal'
        color: Line color
        linestyle: Line style
        alpha: Transparency
    """
    mean_val = np.mean(data)
    median_val = np.median(data)

    if orientation == 'vertical':
        ax.axvline(mean_val, color=color, linestyle=linestyle, alpha=alpha,
                  label=f'Mean: {mean_val:.2f}')
        ax.axvline(median_val, color='orange', linestyle=linestyle, alpha=alpha,
                  label=f'Median: {median_val:.2f}')
    else:  # horizontal
        ax.axhline(mean_val, color=color, linestyle=linestyle, alpha=alpha,
                  label=f'Mean: {mean_val:.2f}')
        ax.axhline(median_val, color='orange', linestyle=linestyle, alpha=alpha,
                  label=f'Median: {median_val:.2f}')

def _handle_overlapping_labels(ax, rotation=45, ha='right'):
    """
    Handle overlapping x-axis labels by rotating them.

    Args:
        ax: Matplotlib axis object
        rotation: Rotation angle in degrees
        ha: Horizontal alignment ('left', 'center', 'right')
    """
    ax.tick_params(axis='x', rotation=rotation, ha=ha)
    plt.tight_layout()

def _create_horizontal_bar_chart(data, x_col, y_col, title, xlabel, ylabel,
                                add_mean_line=True, figsize=(10, 8)):
    """
    Create a horizontal bar chart with optional mean line.

    Args:
        data: DataFrame with data
        x_col: Column for x-axis values
        y_col: Column for y-axis categories
        title: Chart title
        xlabel: X-axis label
        ylabel: Y-axis label
        add_mean_line: Whether to add mean reference line
        figsize: Figure size tuple
    """
    plt.figure(figsize=figsize)

    # Sort data for better visualization
    data_sorted = data.sort_values(x_col, ascending=True)

    bars = plt.barh(data_sorted[y_col], data_sorted[x_col])

    if add_mean_line:
        mean_val = data[x_col].mean()
        plt.axvline(mean_val, color='red', linestyle='--', alpha=0.7,
                   label=f'Mean: {mean_val:.2f}')

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_price_distributions_by_category(df, category_col='main_category', price_col='price'):
    """
    Plot price distributions across categories with mean/median lines.

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

    # Add mean and median lines
    overall_mean = df[price_col].mean()
    overall_median = df[price_col].median()
    plt.axvline(overall_mean, color='red', linestyle='--', alpha=0.7,
               label=f'Overall Mean: {overall_mean:,.0f} VND')
    plt.axvline(overall_median, color='orange', linestyle='--', alpha=0.7,
               label=f'Overall Median: {overall_median:,.0f} VND')

    plt.xlim(0, df[price_col].quantile(0.95))  # Focus on main distribution
    plt.legend()
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
    Plot performance metrics by category using horizontal bars with mean lines.

    Args:
        df (pd.DataFrame): Input dataframe
        category_col (str): Category column
        metrics (list): List of metrics to plot
        show (bool): Whether to display the plot
    """
    fig, axes = plt.subplots(len(metrics), 1, figsize=(12, 6*len(metrics)))

    for i, metric in enumerate(metrics):
        ax = axes[i] if len(metrics) > 1 else axes

        # Calculate category means
        category_means = df.groupby(category_col)[metric].mean().sort_values(ascending=True)

        # Create horizontal bar chart
        bars = ax.barh(category_means.index, category_means.values)

        # Add mean line
        overall_mean = df[metric].mean()
        ax.axvline(overall_mean, color='red', linestyle='--', alpha=0.7,
                  label=f'Overall Mean: {overall_mean:.2f}')

        # Add median line
        overall_median = df[metric].median()
        ax.axvline(overall_median, color='orange', linestyle='--', alpha=0.7,
                  label=f'Overall Median: {overall_median:.2f}')

        ax.set_title(f'Average {metric.replace("_", " ").title()} by Category')
        ax.set_xlabel(metric.replace('_', ' ').title())
        ax.set_ylabel('Category')
        ax.legend()

        # Add value labels on bars
        for j, v in enumerate(category_means.values):
            ax.text(v + max(category_means.values) * 0.01, j, f'{v:.2f}',
                   va='center', fontweight='bold')

    plt.tight_layout()
    if show:
        plt.show()

def create_eda_report(df, interactive=False):
    """
    Generate a comprehensive EDA visualization report.

    Args:
        df (pd.DataFrame): Input dataframe
        interactive (bool): Whether to use interactive Plotly charts
    """
    if interactive:
        print("Generating Interactive EDA Visualization Report...")
        create_interactive_eda_dashboard(df)
    else:
        print("Generating Static EDA Visualization Report...")

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

# ===== INTERACTIVE PLOTLY VISUALIZATIONS =====

def plot_interactive_price_distribution(df, category_col='main_category', price_col='price'):
    """
    Create interactive price distribution plot with Plotly.

    Args:
        df (pd.DataFrame): Input dataframe
        category_col (str): Category column
        price_col (str): Price column
    """
    fig = px.histogram(
        df,
        x=price_col,
        color=category_col,
        marginal="box",
        title="Interactive Price Distribution by Category",
        labels={price_col: "Price (VND)", category_col: "Category"},
        opacity=0.7
    )

    # Add mean and median lines
    mean_price = df[price_col].mean()
    median_price = df[price_col].median()

    fig.add_vline(
        x=mean_price,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Mean: {mean_price:,.0f} VND",
        annotation_position="top right"
    )

    fig.add_vline(
        x=median_price,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Median: {median_price:,.0f} VND",
        annotation_position="top right"
    )

    fig.update_layout(
        xaxis_title="Price (VND)",
        yaxis_title="Count",
        showlegend=True
    )

    fig.show()

def plot_interactive_category_performance(df, category_col='main_category',
                                        metrics=['rating_average', 'quantity_sold', 'price']):
    """
    Create interactive category performance comparison with Plotly.

    Args:
        df (pd.DataFrame): Input dataframe
        category_col (str): Category column
        metrics (list): List of metrics to plot
    """
    # Calculate category statistics
    category_stats = df.groupby(category_col)[metrics].agg(['mean', 'std']).round(2)
    category_stats.columns = [f"{col[0]}_{col[1]}" for col in category_stats.columns]
    category_stats = category_stats.reset_index()

    # Create subplots
    fig = make_subplots(
        rows=len(metrics), cols=1,
        subplot_titles=[f"Average {metric.replace('_', ' ').title()}" for metric in metrics],
        vertical_spacing=0.1
    )

    colors = px.colors.qualitative.Set3

    for i, metric in enumerate(metrics):
        mean_col = f"{metric}_mean"
        std_col = f"{metric}_std"

        fig.add_trace(
            go.Bar(
                x=category_stats[category_col],
                y=category_stats[mean_col],
                error_y=dict(type='data', array=category_stats[std_col]),
                name=metric.replace('_', ' ').title(),
                marker_color=colors[i % len(colors)],
                showlegend=False
            ),
            row=i+1, col=1
        )

        # Add overall mean line
        overall_mean = df[metric].mean()
        fig.add_hline(
            y=overall_mean,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Overall Mean: {overall_mean:.2f}",
            row=i+1, col=1
        )

    fig.update_layout(
        height=300*len(metrics),
        title_text="Category Performance Comparison",
        showlegend=False
    )

    fig.update_xaxes(tickangle=45)

    fig.show()

def plot_interactive_inventory_performance(df, x_col='quantity_sold', y_col='rating_average',
                                         size_col='favourite_count', category_col='main_category',
                                         sample_size=1000):
    """
    Create interactive scatter plot of inventory vs performance with Plotly.

    Args:
        df (pd.DataFrame): Input dataframe
        x_col (str): X-axis column
        y_col (str): Y-axis column
        size_col (str): Size column
        category_col (str): Category column for coloring
        sample_size (int): Number of points to sample for performance
    """
    # Sample data for better performance
    if len(df) > sample_size:
        df_plot = df.sample(sample_size, random_state=42)
    else:
        df_plot = df

    # Create hover text with product info
    hover_text = []
    for idx, row in df_plot.iterrows():
        hover_text.append(
            f"Product: {row.get('name', 'N/A')[:50]}...<br>"
            f"Brand: {row.get('brand', 'N/A')}<br>"
            f"Price: {row.get('price', 'N/A'):,.0f} VND<br>"
            f"Rating: {row.get(y_col, 'N/A')}<br>"
            f"Sales: {row.get(x_col, 'N/A')}"
        )

    fig = px.scatter(
        df_plot,
        x=x_col,
        y=y_col,
        size=size_col,
        color=category_col,
        hover_name="name",
        hover_data=["brand", "price", "rating_average", "review_count"],
        title=f"Interactive {x_col.replace('_', ' ').title()} vs {y_col.replace('_', ' ').title()}",
        labels={
            x_col: x_col.replace('_', ' ').title(),
            y_col: y_col.replace('_', ' ').title(),
            size_col: size_col.replace('_', ' ').title()
        },
        size_max=50
    )

    # Add trend line
    fig.add_trace(
        px.scatter(df_plot, x=x_col, y=y_col, trendline="ols").data[1]
    )

    fig.update_layout(
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title=y_col.replace('_', ' ').title()
    )

    fig.show()

def plot_interactive_brand_comparison(df, brand_col='brand', metric='rating_average', top_n=20):
    """
    Create interactive brand comparison chart.

    Args:
        df (pd.DataFrame): Input dataframe
        brand_col (str): Brand column
        metric (str): Metric to compare
        top_n (int): Number of top brands to show
    """
    # Get top brands by product count
    top_brands = df[brand_col].value_counts().head(top_n).index

    # Filter data for top brands
    df_top = df[df[brand_col].isin(top_brands)]

    # Calculate brand statistics
    brand_stats = df_top.groupby(brand_col)[metric].agg(['mean', 'count', 'std']).round(3)
    brand_stats = brand_stats.reset_index().sort_values('mean', ascending=False)

    fig = px.bar(
        brand_stats,
        x=brand_col,
        y='mean',
        error_y='std',
        color='count',
        title=f"Brand Performance: {metric.replace('_', ' ').title()} (Top {top_n} Brands)",
        labels={
            brand_col: "Brand",
            'mean': f'Average {metric.replace("_", " ").title()}',
            'count': 'Product Count'
        },
        hover_data=['std']
    )

    # Add overall mean line
    overall_mean = df[metric].mean()
    fig.add_hline(
        y=overall_mean,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Overall Mean: {overall_mean:.3f}",
        annotation_position="top right"
    )

    fig.update_xaxes(tickangle=45)
    fig.show()

def create_interactive_eda_dashboard(df):
    """
    Create a comprehensive interactive EDA dashboard.

    Args:
        df (pd.DataFrame): Input dataframe
    """
    print("Generating Interactive EDA Dashboard...")

    # Price distribution
    plot_interactive_price_distribution(df)

    # Category performance
    plot_interactive_category_performance(df)

    # Inventory vs performance
    plot_interactive_inventory_performance(df)

    # Brand comparison
    plot_interactive_brand_comparison(df)

    print("Interactive EDA dashboard generation complete.")