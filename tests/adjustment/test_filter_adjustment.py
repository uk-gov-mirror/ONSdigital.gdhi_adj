import pandas as pd

from gdhi_adj.adjustment.filter_adjustment import (
    filter_by_year,
    filter_lsoa_data,
)


def test_filter_lsoa_data():
    """Test the filter_lsoa_data function."""
    df = pd.DataFrame({
        "lsoa_code": ["E1", "E2", "E3"],
        "lad_code": ["E01", "E02", "E03"],
        "master_flag": [True, None, True],
        "adjust": [True, None, False],
        "year": [2003, 2004, 2005],
        "2002": [10, 20, 30],
    })
    result_df = filter_lsoa_data(df)

    expected_df = pd.DataFrame({
        "lsoa_code": ["E1"],
        "lad_code": ["E01"],
        "adjust": [True],
        "year": [2003],
    })

    pd.testing.assert_frame_equal(result_df, expected_df, check_dtype=False)


def test_filter_by_year():
    """Test the filter_by_year function."""
    df = pd.DataFrame({
        "lad_code": ["E01", "E01", "E01", "E01"],
        "adjust": [True, True, True, True],
        "year": [2010, 2011, 2012, 2013],
        "con_gdhi": [10, 20, 30, 40],
    })

    result_df = filter_by_year(df, start_year=2011, end_year=2012)

    expected_df = pd.DataFrame({
        "lad_code": ["E01", "E01"],
        "adjust": [True, True],
        "year": [2011, 2012],
        "con_gdhi": [20, 30],
    })

    pd.testing.assert_frame_equal(result_df, expected_df, check_dtype=False)
