"""
Configuration file for Business Performance & Inventory Management project.
Contains data paths, column mappings, category definitions, and metric thresholds.
"""

import os

# Data paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
DATA_FILES = [
    'vietnamese_tiki_products_backpacks_suitcases.csv',
    'vietnamese_tiki_products_fashion_accessories.csv',
    'vietnamese_tiki_products_men_bags.csv',
    'vietnamese_tiki_products_men_shoes.csv',
    'vietnamese_tiki_products_women_bags.csv',
    'vietnamese_tiki_products_women_shoes.csv'
]

# Column mappings (if needed for renaming)
COLUMN_MAPPINGS = {
    'original_price': 'original_price',
    'price': 'price',
    'review_count': 'review_count',
    'rating_average': 'rating_average',
    'favourite_count': 'favourite_count',
    'quantity_sold': 'quantity_sold',
    'category': 'category',
    'brand': 'brand',
    'current_seller': 'current_seller',
    'date_created': 'date_created',
    'fulfillment_type': 'fulfillment_type',
    'pay_later': 'pay_later',
    'description': 'description',
    'number_of_images': 'number_of_images',
    'has_video': 'has_video',
    'vnd_cashback': 'vnd_cashback'
}

# Category definitions
MAIN_CATEGORIES = [
    'Backpacks & Suitcases',
    'Fashion Accessories',
    'Men Bags',
    'Men Shoes',
    'Women Bags',
    'Women Shoes'
]

# Metric thresholds
METRIC_THRESHOLDS = {
    'min_reviews_for_reliable_rating': 5,
    'high_rating_threshold': 4.5,
    'low_stock_threshold': 10,  # Assuming quantity_sold represents current stock
    'top_seller_threshold': 1000,  # Sales volume
    'discount_significant_threshold': 0.1  # 10% discount
}

# Business constants
CURRENCY = 'VND'
ENCODING = 'utf-8'