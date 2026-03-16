"""
Report generator for Business Performance & Inventory Management.
Generates sample reports with key findings and visualizations.
"""

import sys
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Add src to path
sys.path.append('../src')

from preprocessing import preprocess_data
from inventory_analysis import generate_inventory_report
from performance_analysis import generate_performance_report
from visualization import plot_category_performance, plot_correlation_matrix
from metrics import calculate_roi, calculate_customer_satisfaction_score
from utils import format_currency, create_log_entry

def generate_summary_report(df, inventory_report, performance_report, output_dir='reports'):
    """
    Generate a comprehensive summary report.

    Args:
        df (pd.DataFrame): Preprocessed dataframe
        inventory_report (dict): Inventory analysis results
        performance_report (dict): Performance analysis results
        output_dir (str): Output directory for reports
    """
    os.makedirs(output_dir, exist_ok=True)

    report_content = f"""
# Business Performance & Inventory Management Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

This report analyzes {inventory_report['total_products']:,} products across {len(df['main_category'].unique())} categories from Tiki e-commerce platform.

### Key Metrics
- **Total Products**: {inventory_report['total_products']:,}
- **Average Performance Score**: {performance_report['avg_performance_score']:.3f}
- **Slow Movers**: {inventory_report['slow_movers_count']:,} ({inventory_report['slow_movers_count']/inventory_report['total_products']*100:.1f}%)
- **Fast Movers**: {inventory_report['fast_movers_count']:,} ({inventory_report['fast_movers_count']/inventory_report['total_products']*100:.1f}%)
- **Top Category**: {performance_report['top_category']}
- **Top Brand**: {performance_report.get('top_brand', 'N/A')}

## Inventory Analysis

### Turnover Metrics
- Average Turnover Rate: {inventory_report['avg_turnover_rate']:.2f} units/day
- Top Category by Sales: {inventory_report['top_category_by_sales']}

### Health Distribution
{chr(10).join([f"- {k}: {v}" for k, v in inventory_report['health_distribution'].items()])}

### ABC Classification
- Category A (High Value): {inventory_report['abc_distribution'].get('A', 0):,} products
- Category B (Medium Value): {inventory_report['abc_distribution'].get('B', 0):,} products  
- Category C (Low Value): {inventory_report['abc_distribution'].get('C', 0):,} products

### Stock-out Risk
{chr(10).join([f"- {k}: {v}" for k, v in inventory_report['stockout_risk_distribution'].items()]) if inventory_report['stockout_risk_distribution'] else "Time-based data not available for stock-out analysis"}

## Performance Analysis

### Top Performing Products
{chr(10).join([f"1. {p.get('name', p.get('id', 'Unknown'))} (Score: {p['performance_score']:.3f})" for p in performance_report['top_performing_products'][:5]])}

### Pareto Analysis (80/20 Rule)
Top category analysis shows {len([c for c in performance_report['pareto_analysis'].values() if c['pareto_ratio'] < 0.25])} categories following 80/20 rule closely.

### Discount Effectiveness
- Correlation between discount % and sales: {performance_report['discount_effectiveness']['correlations'].get('discount_pct', {}).get('quantity_sold', 0):.3f}
- High discount products (>30%): {performance_report['discount_effectiveness']['key_insights']['high_discount_products']:,}

### Brand Equity Analysis
- Branded products premium: {format_currency(performance_report['brand_equity']['brand_premium']['price_difference'])} higher price
- Rating difference: {performance_report['brand_equity']['brand_premium']['rating_difference']:.2f} points

## Advanced Recommendations

### Inventory Optimization
1. **ABC Focus**: Prioritize Category A products ({inventory_report['abc_distribution'].get('A', 0):,} items) for tight inventory control
2. **Stock-out Prevention**: Monitor {inventory_report['stockout_risk_distribution'].get('High', 0)} high-risk products closely
3. **SKU Rationalization**: Review {inventory_report['sku_rationalization']['total_skus_to_review']:,} low-performing SKUs for potential reduction

### Performance Enhancement
1. **Pareto Strategy**: Focus marketing on top 20% products driving 80% of value in key categories
2. **Discount Optimization**: Analyze discount impact - current correlation suggests { "strong" if abs(performance_report['discount_effectiveness']['correlations'].get('discount_pct', {}).get('quantity_sold', 0)) > 0.3 else "limited"} relationship with sales
3. **Brand Strategy**: Leverage top brands for premium positioning

### Strategic Insights
1. Customer satisfaction scores range from {df['composite_score'].min():.1f} to {df['composite_score'].max():.1f}
2. {inventory_report['sku_rationalization']['total_skus_to_review']:,} SKUs identified for potential rationalization
3. Brand premium strategy viable with {format_currency(performance_report['brand_equity']['brand_premium']['price_difference'])} price differential

---
*Advanced analysis report generated automatically from Tiki product data*
*Includes Pareto analysis, ABC classification, discount effectiveness, and brand equity insights*
"""

    # Save text report
    with open(os.path.join(output_dir, 'summary_report.md'), 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"Summary report saved to {output_dir}/summary_report.md")

def generate_visualization_report(df, output_dir='reports'):
    """
    Generate key visualizations for the report.

    Args:
        df (pd.DataFrame): Preprocessed dataframe
        output_dir (str): Output directory
    """
    os.makedirs(output_dir, exist_ok=True)

    # Set style
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")

    # 1. Category Performance Chart
    plt.figure(figsize=(12, 6))
    plot_category_performance(df)
    plt.savefig(os.path.join(output_dir, 'category_performance.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Correlation Matrix
    plt.figure(figsize=(10, 8))
    numeric_cols = ['price', 'rating_average', 'review_count', 'favourite_count',
                   'quantity_sold', 'discount_pct', 'composite_score']
    available_cols = [col for col in numeric_cols if col in df.columns]
    plot_correlation_matrix(df, available_cols)
    plt.savefig(os.path.join(output_dir, 'correlation_matrix.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Price Distribution by Category
    plt.figure(figsize=(12, 6))
    for category in df['main_category'].unique():
        subset = df[df['main_category'] == category]
        sns.kdeplot(data=subset, x='price', label=category, fill=True, alpha=0.3)
    plt.title('Price Distributions by Category')
    plt.xlabel('Price (VND)')
    plt.ylabel('Density')
    plt.legend()
    plt.xlim(0, df['price'].quantile(0.95))
    plt.savefig(os.path.join(output_dir, 'price_distributions.png'), dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Visualization reports saved to {output_dir}/")

def main():
    """Main function to generate all reports."""
    print("Starting report generation...")

    # Load and preprocess data
    df = preprocess_data()

    # Generate analysis reports
    inventory_report, df_inv = generate_inventory_report(df)
    performance_report, df_perf = generate_performance_report(df)

    # Generate summary report
    generate_summary_report(df, inventory_report, performance_report)

    # Generate visualizations
    generate_visualization_report(df)

    print("All reports generated successfully!")
    print("Check the reports/ directory for output files.")

if __name__ == "__main__":
    main()