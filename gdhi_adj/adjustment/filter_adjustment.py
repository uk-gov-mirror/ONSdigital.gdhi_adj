"""Module for filtering adjustment data in the gdhi_adj project."""

import pandas as pd


def filter_lsoa_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter LSOA data to keep only relevant columns and rows.

    Args:
        df (pd.DataFrame): Input DataFrame containing LSOA data.

    Returns:
        pd.DataFrame: Filtered DataFrame with only relevant columns and rows.
    """
    df = df[df["adjust"].astype("boolean").fillna(False)]

    cols_to_keep = [
        "lsoa_code",
        "lad_code",
        "adjust",
        "year",
    ]

    df = df[cols_to_keep]

    return df


def filter_by_year(
    df: pd.DataFrame, start_year: int, end_year: int
) -> pd.DataFrame:
    """
    Filter DataFrame by a range of years inclusively.
    Args:
        df (pd.DataFrame): Input DataFrame containing year data.
        start_year (int): Start year for filtering (inclusive).
        end_year (int): End year for filtering (inclusive).
    Returns:
        pd.DataFrame: Filtered DataFrame containing only rows within the year
        range.
    """
    df = df[(df["year"] >= start_year) & (df["year"] <= end_year)]

    df = df.reset_index(drop=True)

    return df
