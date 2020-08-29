import pandas as pd


def create_yearly_table(df):
    """reads in source csv file, transforms data and merges with locations table"""
    df.rename(columns={"Zählstelle        Inbetriebnahme": "timestamp"}, inplace=True)
    df.timestamp = pd.to_datetime(df.timestamp).copy()
    stacked = df.stack().reset_index()
    merged = pd.merge(
        stacked, df.timestamp.reset_index(), "left", left_on="level_0", right_on="index"
    ).drop(columns=["level_0", "index"])
    temp_df = (
        merged[merged.level_1 != "timestamp"]
        .set_index("timestamp")
        .rename(columns={"level_1": "station", 0: "total_bikes"})
    )
    temp_df["total_bikes"] = temp_df["total_bikes"].astype(int).copy()
    temp_df.station = temp_df.station.str[:-11].copy()
    temp_df.station = temp_df.station.str.strip().copy()
    temp_df.station.replace("17-SZ-BRE-O", "17-SK-BRE-O", inplace=True)
    temp_df.station.replace("17-SZ-BRE-W", "17-SK-BRE-W", inplace=True)
    temp_df["hour"] = temp_df.index.hour
    temp_df["hour_str"] = temp_df.hour.astype(str) + " Uhr"
    temp_df["weekday"] = temp_df.index.weekday.copy()
    temp_df["day_name"] = temp_df.index.day_name().copy()
    temp_df["month"] = temp_df.index.month.copy()
    temp_df["month_name"] = temp_df.index.month_name().copy()
    temp_df["year"] = temp_df.index.year.copy()
    final_geo = (
        pd.merge(
            temp_df.reset_index(),
            locations.drop(columns="Installationsdatum"),
            "left",
            left_on="station",
            right_on="Zählstelle",
        )
        .drop(columns=["Zählstelle"])
        .rename(
            columns={
                "Beschreibung - Fahrtrichtung": "description",
                "Breitengrad": "lat",
                "Längengrad": "lon",
            }
        )
        .set_index("timestamp")
    )
    return final_geo


def transform_concat_dataframes(dataframes_list):
    """transform all loaded dataframes and concat them"""
    processed_dataframes = []
    for dataframe in dataframes_list:
        processed_dataframes.append(create_yearly_table(dataframe))
    return pd.concat(processed_dataframes)


if __name__ == "__main__":
    locations = pd.read_excel(
        "gesamtdatei_stundenwerte_2012-2019.xlsx", sheet_name="Standortdaten"
    )
    dataframes = []
    for year in range(2017, 2020):
        dataframes.append(
            pd.read_excel(
                "gesamtdatei_stundenwerte_2012-2019.xlsx",
                sheet_name=f"Jahresdatei {year}",
            )
        )
    final_table = transform_concat_dataframes(dataframes)
    final_table.to_csv("berlin_bikedata_2017-2019.csv")
