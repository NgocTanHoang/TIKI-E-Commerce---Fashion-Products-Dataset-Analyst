"""
Preprocessing module for Tiki product data.
Handles data loading, cleaning, and feature engineering.
"""

import pandas as pd
import numpy as np
import glob
import os
from config import DATA_DIR, DATA_FILES, ENCODING

def load_and_combine_datasets(data_dir=DATA_DIR, files=DATA_FILES, encoding=ENCODING):
    """
    Load and combine all CSV files from the data directory.

    Args:
        data_dir (str): Path to data directory
        files (list): List of CSV filenames
        encoding (str): File encoding

    Returns:
        pd.DataFrame: Combined dataframe
    """
    file_paths = [os.path.join(data_dir, f) for f in files]
    dfs = []
    for file_path in file_paths:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, encoding=encoding)
            dfs.append(df)
        else:
            print(f"Warning: {file_path} not found")

    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        print(f"Loaded {len(dfs)} files, total shape: {combined_df.shape}")
        return combined_df
    else:
        raise ValueError("No data files found")

def clean_basic_columns(df):
    """
    Remove unnecessary columns like 'Unnamed: 0'.

    Args:
        df (pd.DataFrame): Input dataframe

    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    columns_to_drop = [col for col in df.columns if col.startswith('Unnamed')]
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)
        print(f"Dropped columns: {columns_to_drop}")
    return df

def handle_missing_values(df, strategy='drop'):
    """
    Handle missing values in the dataframe.

    Args:
        df (pd.DataFrame): Input dataframe
        strategy (str): 'drop' to remove rows with NaN, 'fill' to fill with mean/mode

    Returns:
        pd.DataFrame: Dataframe with handled missing values
    """
    null_count = df.isnull().sum().sum()
    if null_count > 0:
        print(f"Found {null_count} null values")
        if strategy == 'drop':
            initial_shape = df.shape
            df = df.dropna()
            print(f"Dropped {initial_shape[0] - df.shape[0]} rows with null values")
        elif strategy == 'fill':
            # Fill numeric columns with mean, categorical with mode
            for col in df.columns:
                if df[col].dtype in ['int64', 'float64']:
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    df[col] = df[col].fillna(df[col].mode().iloc[0] if not df[col].mode().empty else 'Unknown')
            print("Filled missing values")
    else:
        print("No null values found")
    return df

def clean_duplicates_by_id(df, id_column='id'):
    """
    Remove duplicate rows based on ID column.

    Args:
        df (pd.DataFrame): Input dataframe
        id_column (str): Column to check for duplicates

    Returns:
        pd.DataFrame: Dataframe without duplicates
    """
    initial_shape = df.shape
    df = df.drop_duplicates(subset=id_column)
    duplicates_removed = initial_shape[0] - df.shape[0]
    if duplicates_removed > 0:
        print(f"Removed {duplicates_removed} duplicate rows")
    else:
        print("No duplicates found")
    return df

def validate_price_consistency(df, original_price_col='original_price', price_col='price'):
    """
    Validate that original_price >= price and flag inconsistencies.

    Args:
        df (pd.DataFrame): Input dataframe
        original_price_col (str): Original price column
        price_col (str): Current price column

    Returns:
        pd.DataFrame: Dataframe with validation results
    """
    inconsistent = df[df[original_price_col] < df[price_col]]
    if len(inconsistent) > 0:
        print(f"Found {len(inconsistent)} rows with price inconsistencies")
        print("Inconsistent rows:")
        print(inconsistent[[original_price_col, price_col]])
        # Could raise error or handle differently
    else:
        print("All price relationships are consistent")
    return df

def normalize_categories(df, category_col='category'):
    """
    Normalize category format (handle Main/Sub vs Main).

    Args:
        df (pd.DataFrame): Input dataframe
        category_col (str): Category column

    Returns:
        pd.DataFrame: Dataframe with normalized categories
    """
    # Split category into main and sub if '/' exists
    df['main_category'] = df[category_col].str.split('/').str[0].str.strip()
    df['sub_category'] = df[category_col].str.split('/').str[1].str.strip() if '/' in df[category_col].iloc[0] else None
    print("Normalized categories into main_category and sub_category")
    return df

def extract_description_features(df, description_col='description'):
    """
    Extract features from product descriptions (length, keywords, etc.).

    Args:
        df (pd.DataFrame): Input dataframe
        description_col (str): Description column

    Returns:
        pd.DataFrame: Dataframe with additional description features
    """
    df['description_length'] = df[description_col].fillna('').str.len()
    # Could add keyword extraction, sentiment analysis, etc.
    print("Extracted description length feature")
    return df

def engineer_features(df):
    """
    Engineer additional business-relevant features.

    Args:
        df (pd.DataFrame): Input dataframe

    Returns:
        pd.DataFrame: Dataframe with engineered features
    """
    # Discount percentage
    df['discount_pct'] = (df['original_price'] - df['price']) / df['original_price']
    df['discount_pct'] = df['discount_pct'].clip(0, 1)  # Ensure between 0 and 1

    # Product age (assuming date_created is creation date)
    if 'date_created' in df.columns:
        df['date_created'] = pd.to_datetime(df['date_created'], errors='coerce')
        df['product_age_days'] = (pd.Timestamp.now() - df['date_created']).dt.days
        print("Engineered discount_pct and product_age_days features")
    else:
        print("date_created column not found, skipping age calculation")

    # Composite score (example: weighted rating)
    df['composite_score'] = (
        df['rating_average'] * 0.4 +
        (df['review_count'] / df['review_count'].max()) * 0.3 +
        (df['favourite_count'] / df['favourite_count'].max()) * 0.3
    )

    return df

def preprocess_data(data_dir=DATA_DIR, files=DATA_FILES):
    """
    Complete preprocessing pipeline.

    Args:
        data_dir (str): Data directory path
        files (list): List of CSV files

    Returns:
        pd.DataFrame: Fully preprocessed dataframe
    """
    print("Starting data preprocessing...")

    # Load data
    df = load_and_combine_datasets(data_dir, files)

    # Clean columns
    df = clean_basic_columns(df)

    # Handle missing values
    df = handle_missing_values(df)

    # Remove duplicates
    df = clean_duplicates_by_id(df)

    # Validate prices
    df = validate_price_consistency(df)

    # Normalize categories
    df = normalize_categories(df)

    # Extract description features
    df = extract_description_features(df)

    # Engineer features
    df = engineer_features(df)

    print(f"Preprocessing complete. Final shape: {df.shape}")
    return df