"""helper function for polar chart"""

import pandas as pd


def prepare_data_for_polar(complete_df, CATEGORY, CAT_SORTERS, station):
    """creates dataframes for median and max values for polar chart"""
    df_median = (
        complete_df[(complete_df.description == station)]
        .groupby([CATEGORY, CAT_SORTERS[CATEGORY]])[["total_bikes"]]
        .median()
        .reset_index()
        .sort_values(CAT_SORTERS[CATEGORY])
    )
    df_median["location"] = station
    df_max = (
        complete_df[(complete_df.description == station)]
        .groupby([CATEGORY, CAT_SORTERS[CATEGORY]])[["total_bikes"]]
        .max()
        .reset_index()
        .sort_values(CAT_SORTERS[CATEGORY])
    )
    df_max["location"] = station
    radialrange_dict = {
        "max": df_max["total_bikes"].max(),
        "median": df_median["total_bikes"].max(),
    }
    categories = df_median[CATEGORY]
    return df_median, df_max, radialrange_dict, categories
