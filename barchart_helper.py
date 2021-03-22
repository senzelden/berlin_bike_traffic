"""helper functions for bar chart"""

import pandas as pd


class Frequency:
    def __init__(self, frequency, frequency_dict, location_id):
        self.frequency = frequency
        self.frequency_short = frequency_dict["frequency"][frequency]["short"]
        self.d3_format = frequency_dict["frequency"][frequency]["d3_format"]
        self.location_id = int(location_id)
        self.hovertext = f"<b>{self.frequency}</b>: %{{x|{self.d3_format}}}<br><b>Total Bikes</b>: %{{y}}"


def prepare_dataframe(df):
    """updates dataframe for barchart"""
    df["station_short"] = df.station.str.split("-", n=1, expand=True).rename(
        columns={0: "station_short"}
    )["station_short"]
    df["timestamp"] = pd.to_datetime(df.timestamp)
    return df


def get_parts_for_barchart(df, barchart_object):
    """returns barchart_df, barchart_title"""
    # .set_index("timestamp")
    barchart_df = (
        df.groupby(["description", "station_short"])[["total_bikes"]].resample(barchart_object.frequency_short).sum().reset_index()
    )
    street_names = " / ".join(
        barchart_df[barchart_df.station_short == barchart_object.location_id][
            "description"
        ].unique()
    )
    barchart_title = f"Data for Bicycle Counter {street_names}"
    return barchart_df, barchart_title


frequency_dict = {
    "frequency": {
        "Day": {"short": "D", "d3_format": "%b %d, %Y (%a)"},
        "Week": {"short": "W", "d3_format": "%b %d, %Y"},
        "Month": {"short": "M", "d3_format": "%B %Y"},
        "Year": {"short": "Y", "d3_format": "%Y"},
    }
}
streets_dict = {
    "Alberichstraße": "24",
    "Berliner Straße": "10",
    "Breitenbachplatz": "17",
    "Frankfurter Allee": "06",
    "Invalidenstraße": "03",
    "Jannowitzbrücke": "02",
    "Kaisersteg": "23",
    "Klosterstraße": "15",
    "Mariendorfer Damm": "20",
    "Markstraße": "27",
    "Maybachufer": "21",
    "Monumentenstraße": "19",
    "Oberbaumbrücke": "05",
    "Paul-und-Paula-Uferweg": "26",
    "Prinzregentenstraße": "13",
    "Schwedter Steg": "12",
    "Yorckstraße": "18",
}
