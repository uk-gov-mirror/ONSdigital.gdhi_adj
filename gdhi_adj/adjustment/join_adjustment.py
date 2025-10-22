"""Module for joining adjustment data in the gdhi_adj project."""

import pandas as pd


def join_analyst_constrained_data(
    df_constrained: pd.DataFrame,
    df_analyst: pd.DataFrame,
    transaction_name: str,
) -> pd.DataFrame:
    """
    Join analyst data to constrained data based on LSOA code and LAD code.

    Args:
        df_constrained (pd.DataFrame): DataFrame containing constrained data.
        df_analyst (pd.DataFrame): DataFrame containing analyst data.
        transaction_name (str): Name of the transaction to filter constrained
        data.

    Returns:
        pd.DataFrame: Joined DataFrame with relevant columns.
    """
    df_constrained = df_constrained[
        df_constrained["transaction"] == transaction_name
    ]

    df = df_analyst.merge(
        df_constrained,
        on=["lad_code"],
        how="left",
    )

    # Obtain list of columns to rename
    exclude_cols = [
        "lsoa_code",
        "lad_code",
        "adjust",
        "year",
    ]
    included_cols = [col for col in df.columns if col not in exclude_cols]

    # Create a renaming dictionary with prefix
    rename_dict = {col: f"CON_{col}" for col in included_cols}

    df = df.rename(columns=rename_dict)

    if df["adjust"].sum() != df_analyst["adjust"].sum():
        raise ValueError(
            "Number of rows to adjust between analyst and constrained data"
            " do not match."
        )
    breakpoint()
    if df.shape[0] != df_constrained.shape[0]:
        raise ValueError(
            "Number of rows of constrained data after join has increased."
        )

    return df


def join_analyst_unconstrained_data(
    df_unconstrained: pd.DataFrame, df_analyst: pd.DataFrame
) -> pd.DataFrame:
    """
    Join analyst data to unconstrained data based on LSOA code and LAD code.

    Args:
        df_unconstrained (pd.DataFrame): DataFrame with unconstrained data.
        df_analyst (pd.DataFrame): DataFrame containing analyst data.

    Returns:
        pd.DataFrame: Joined DataFrame with relevant columns.
    """
    df = df_unconstrained.merge(
        df_analyst,
        on=["lsoa_code", "lad_code"],
        how="left",
    )

    df["adjust"] = df["adjust"].where(pd.notnull(df["adjust"]), False)

    if df["adjust"].sum() != df_analyst["adjust"].sum():
        raise ValueError(
            "Number of rows to adjust between analyst and unconstrained data"
            " do not match."
        )

    if df.shape[0] != df_unconstrained.shape[0]:
        raise ValueError(
            "Number of rows of unconstrained data after join has increased."
        )

    return df
