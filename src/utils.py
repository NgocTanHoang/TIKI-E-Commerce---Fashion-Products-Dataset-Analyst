"""
Utilities module for helper functions.
Contains formatting, text processing, and logging utilities.
"""

import pandas as pd
import numpy as np
import re
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/analysis.log'),
        logging.StreamHandler()
    ]
)

def format_currency(amount, currency='VND', locale='vi_VN'):
    """
    Format currency amount with proper localization.

    Args:
        amount (float): Amount to format
        currency (str): Currency code
        locale (str): Locale for formatting

    Returns:
        str: Formatted currency string
    """
    try:
        if currency == 'VND':
            # Format VND with thousand separators
            return f"{amount:,.0f} VND"
        else:
            return f"{currency} {amount:,.2f}"
    except:
        return f"{amount} {currency}"

def clean_vietnamese_text(text):
    """
    Clean and normalize Vietnamese text.

    Args:
        text (str): Input text

    Returns:
        str: Cleaned text
    """
    if not isinstance(text, str):
        return str(text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())

    # Normalize common Vietnamese characters
    text = text.replace('đ', 'd').replace('Đ', 'D')

    return text

def extract_keywords_from_description(description, max_keywords=5):
    """
    Extract potential keywords from product description.

    Args:
        description (str): Product description
        max_keywords (int): Maximum number of keywords to extract

    Returns:
        list: List of extracted keywords
    """
    if not isinstance(description, str) or not description:
        return []

    # Simple keyword extraction (can be enhanced with NLP)
    words = clean_vietnamese_text(description).lower().split()

    # Remove common stop words (Vietnamese)
    stop_words = {'của', 'là', 'và', 'có', 'trong', 'được', 'cho', 'với', 'như', 'từ', 'đến', 'theo'}
    keywords = [word for word in words if len(word) > 2 and word not in stop_words]

    # Return most common keywords
    from collections import Counter
    word_counts = Counter(keywords)
    return [word for word, _ in word_counts.most_common(max_keywords)]

def safe_divide(numerator, denominator, default=0):
    """
    Safe division to avoid division by zero.

    Args:
        numerator: Numerator value
        denominator: Denominator value
        default: Default value if division by zero

    Returns:
        float: Division result or default
    """
    try:
        return numerator / denominator if denominator != 0 else default
    except:
        return default

def calculate_percentage(part, total, decimals=2):
    """
    Calculate percentage safely.

    Args:
        part: Part value
        total: Total value
        decimals: Decimal places

    Returns:
        float: Percentage
    """
    return round(safe_divide(part, total) * 100, decimals)

def create_log_entry(message, level='info'):
    """
    Create a log entry.

    Args:
        message (str): Log message
        level (str): Log level (debug, info, warning, error)
    """
    logger = logging.getLogger(__name__)

    if level == 'debug':
        logger.debug(message)
    elif level == 'info':
        logger.info(message)
    elif level == 'warning':
        logger.warning(message)
    elif level == 'error':
        logger.error(message)
    else:
        logger.info(message)

def validate_dataframe(df, required_columns=None):
    """
    Validate dataframe structure and required columns.

    Args:
        df (pd.DataFrame): Dataframe to validate
        required_columns (list): List of required column names

    Returns:
        dict: Validation results
    """
    results = {
        'is_valid': True,
        'issues': [],
        'shape': df.shape,
        'columns': list(df.columns)
    }

    if df.empty:
        results['is_valid'] = False
        results['issues'].append('DataFrame is empty')
        return results

    if required_columns:
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            results['is_valid'] = False
            results['issues'].append(f'Missing required columns: {missing_columns}')

    # Check for null values
    null_counts = df.isnull().sum()
    total_nulls = null_counts.sum()
    if total_nulls > 0:
        results['issues'].append(f'Found {total_nulls} null values across {len(null_counts[null_counts > 0])} columns')

    return results

def sample_dataframe(df, n=5, random_state=42):
    """
    Get a sample of the dataframe for inspection.

    Args:
        df (pd.DataFrame): Input dataframe
        n (int): Number of samples
        random_state (int): Random state for reproducibility

    Returns:
        pd.DataFrame: Sample dataframe
    """
    if len(df) <= n:
        return df
    return df.sample(n=n, random_state=random_state)

def time_function_execution(func):
    """
    Decorator to time function execution.

    Args:
        func: Function to time

    Returns:
        wrapper function
    """
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()

        execution_time = (end_time - start_time).total_seconds()
        create_log_entry(f"{func.__name__} executed in {execution_time:.2f} seconds")

        return result
    return wrapper

def export_to_csv(df, filename, output_dir='data/processed/'):
    """
    Export dataframe to CSV with proper encoding.

    Args:
        df (pd.DataFrame): Dataframe to export
        filename (str): Output filename
        output_dir (str): Output directory
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    create_log_entry(f"Data exported to {filepath}")

def load_from_csv(filename, input_dir='data/'):
    """
    Load dataframe from CSV with proper encoding.

    Args:
        filename (str): Input filename
        input_dir (str): Input directory

    Returns:
        pd.DataFrame: Loaded dataframe
    """
    import os
    filepath = os.path.join(input_dir, filename)

    if os.path.exists(filepath):
        df = pd.read_csv(filepath, encoding='utf-8-sig')
        create_log_entry(f"Data loaded from {filepath}")
        return df
    else:
        create_log_entry(f"File not found: {filepath}", 'warning')
        return pd.DataFrame()