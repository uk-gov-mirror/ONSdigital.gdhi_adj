"""Module for flagging preprocessing data in the gdhi_adj project."""

import numpy as np
import pandas as pd


def flag_rollback_years(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flags years where the GDHI has rolled back from future years.
    Typically 2010-2014 has 2015 data copied to them as it is missing.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with an additional 'rollback_flag' column.
    """
    # Create a mask for years where the GDHI has rolled back
    # 2015 is included due to forward percentage change column
    rollback_mask = (
        (df["backward_pct_change"] == 1.0) | (df["forward_pct_change"] == 1.0)
    ) & (df["year"].between(2010, 2014))

    # Create a new column 'rollback_flag' based on the mask
    df["rollback_flag"] = np.where(rollback_mask, True, False)

    return df


def create_master_flag(
    df: pd.DataFrame, zscore_calculation: bool, iqr_calculation: bool
) -> pd.DataFrame:
    """
    Creates a master flag based on z score and IQR flag columns.

    Args:
        df (pd.DataFrame): The input DataFrame.
        zscore_calculation (bool): Whether z-score calculation is performed.
        iqr_calculation (bool): Whether IQR calculation is performed.

    Returns:
        pd.DataFrame: The DataFrame with an additional 'master_flag' columns.
    """
    if zscore_calculation:
        # Create list of zscore flag columns (these should be the only columns
        # prefixed with 'z_')
        z_score_cols = [col for col in df.columns if col.startswith("z_")]
        # Create a master flag that is True if any of the IQR columns are True
        # Only group by LSOA as if any year is flagged, the LSOA is flagged
        z_count = df.groupby("lsoa_code").agg(
            {col: "sum" for col in z_score_cols}
        )
        z_count["master_z_flag"] = (z_count[z_score_cols] >= 1).sum(
            axis=1
        ) >= 1

        # Join the master flags back to the original DataFrame
        df = df.join(z_count[["master_z_flag"]], on="lsoa_code", how="left")

    if iqr_calculation:
        # Create list of IQR flag columns (these should be the only columns
        # prefixed with 'iqr_')
        iqr_score_cols = [col for col in df.columns if col.startswith("iqr_")]
        # Create a master flag that is True if any of the IQR columns are True
        # Only group by LSOA as if any year is flagged, the LSOA is flagged
        iqr_count = df.groupby("lsoa_code").agg(
            {col: "sum" for col in iqr_score_cols}
        )
        iqr_count["master_iqr_flag"] = (iqr_count[iqr_score_cols] >= 1).sum(
            axis=1
        ) >= 1

        # Join the master flags back to the original DataFrame
        df = df.join(
            iqr_count[["master_iqr_flag"]], on="lsoa_code", how="left"
        )

    # Create a master flag that is True if any master flag is True.
    flag_cols = [col for col in df.columns if col.startswith("master_")]
    df["master_flag"] = df[flag_cols].all(axis=1)

    return df


def add_config_parameter_cols(
    df: pd.DataFrame,
    zscore_lower_threshold: float,
    zscore_upper_threshold: float,
    iqr_lower_quantile: float,
    iqr_upper_quantile: float,
    iqr_multiplier: float,
) -> pd.DataFrame:
    """
    Adds configuration parameter columns to the DataFrame for reference.

    Args:
        df (pd.DataFrame): The input DataFrame.
        zscore_lower_threshold (float): Z-score lower threshold.
        zscore_upper_threshold (float): Z-score upper threshold.
        iqr_lower_quantile (float): IQR lower quantile.
        iqr_upper_quantile (float): IQR upper quantile.
        iqr_multiplier (float): IQR multiplier.
    Returns:
        pd.DataFrame: DataFrame with configuration parameter columns.
    """
    df["zscore_lower_threshold"] = zscore_lower_threshold
    df["zscore_upper_threshold"] = zscore_upper_threshold
    df["iqr_lower_quantile"] = iqr_lower_quantile
    df["iqr_upper_quantile"] = iqr_upper_quantile
    df["iqr_multiplier"] = iqr_multiplier

    return df
