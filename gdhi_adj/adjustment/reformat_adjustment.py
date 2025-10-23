"""Module for joining adjustment data in the gdhi_adj project."""

import numpy as np
import pandas as pd


def reformat_adjust_col(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reformat data within the adjust column.

    Args:
        df (pd.DataFrame): Input DataFrame to be reformatted.

    Returns:
        pd.DataFrame: DataFrame with reformatted columns.
    """
    conditions = [df["adjust"] == "TRUE"]
    descriptors = [True]
    df["adjust"] = np.select(conditions, descriptors, default=False)

    df["adjust"] = df["adjust"].astype("boolean")

    return df


def reformat_year_col(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reformat data within the year column.

    Args:
        df (pd.DataFrame): Input DataFrame to be reformatted.

    Returns:
        pd.DataFrame: DataFrame with reformatted columns.
    """
    # Check for rows where adjust column is marked true to be adjusted but
    # year has not been populated
    mismatch = df["adjust"] & df["year"].isnull()

    if mismatch.any():
        raise ValueError(
            "Mismatch: adjust column flagged but no year to adjust has been "
            "provided."
        )

    df["year"] = df["year"].apply(lambda x: x.replace(" ", ""))

    df["year"] = df["year"].apply(lambda x: x.split(","))

    return df
