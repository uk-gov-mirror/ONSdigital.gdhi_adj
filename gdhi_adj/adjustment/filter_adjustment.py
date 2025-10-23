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
    df = df[df["adjust"]]

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


def filter_anomaly_list(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a list of anomalies in the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing data to check for anomalies.

    Returns:
        pd.DataFrame: DataFrame with unique anomalies listed.
    """
    anomaly_lsoa = df[df["adjust"]]
    anomaly_lsoa = (
        anomaly_lsoa[["lsoa_code", "year_to_adjust"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    return anomaly_lsoa
