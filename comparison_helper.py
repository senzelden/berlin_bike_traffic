import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class ComparisonBetweenStations:
    """Parameters for comparison between stations"""

    def __init__(self, years, aggregation):
        self.years = years
        if len(self.years) > 1:
            self.years_string = "20" + "/".join(
                [str(year)[2:] for year in sorted(self.years)]
            )
        else:
            self.years_string = "".join(str(self.years[0]))
        self.aggregation = aggregation


def prepare_comparison_df(df):
    """updates dataframe for barchart"""
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)
    return df


def aggregate(df, comparison):
    """returns aggregated dataframe"""
    if comparison.aggregation == "sum":
        bikes_df = (
            df[df.index.year.isin(comparison.years)]
            .groupby("description")[["total_bikes"]]
            .sum()
            .sort_values("total_bikes", ascending=True)
        )
    elif comparison.aggregation == "mean":
        bikes_df = (
            df[df.index.year.isin(comparison.years)]
            .groupby("description")[["total_bikes"]]
            .resample("D")
            .sum()
            .reset_index()
            .groupby("description")[["total_bikes"]]
            .mean()
            .sort_values("total_bikes", ascending=True)
        )
    return bikes_df


def get_key(my_dict, val):
    """function to return key for any value"""
    for key, value in my_dict.items():
        if val == value:
            return key

    return "key doesn't exist"


def map_colors(dataframe, station_name):
    """returns list of y values for horizontal bar and color map"""
    stations_dict = dataframe.reset_index()['description'].to_dict()
    colors = ['lightslategray', ] * len(stations_dict)
    colors[get_key(stations_dict, station_name)] = 'lightgreen'
    stations_list = stations_dict.values()
    color_map = dict(zip(stations_list, colors))
    return stations_list, color_map


if __name__ == "__main__":
    df = pd.read_csv("berlin_bikedata_2017-2019.csv")
    prepare_comparison_df(df)
    comparison = ComparisonBetweenStations([2019], "mean")
    bikes_df = aggregate(df, comparison)

    # Set general style for plotly graphs
    px.defaults.template = "ggplot2"
    px.defaults.color_continuous_scale = px.colors.sequential.Plasma_r

    # Barchart with Total Bikes by year and bicycle counter
    fig = px.bar(
        bikes_df.reset_index(),
        x="total_bikes",
        y="description",
        color="total_bikes",
        orientation="h",
        labels={"total_bikes": "Total Bikes", "description": "Bicycle Counter"},
    )
    fig.add_annotation(
        text=f"{comparison.years_string}",
        xref="paper",
        yref="paper",
        x=1,
        y=0,
        showarrow=False,
        opacity=0.1,
        font=dict(family="Arial", size=100, color="black"),
    )
    fig.show()

    # sum_total_bikes = int(
    #     df[df.index.year.isin(comparison.years)].groupby('description')[['total_bikes']].sum().groupby('description')[
    #         ['total_bikes']].sum().sum())
    # # Draw indicator
    # fig = go.Figure()
    # fig.add_trace(go.Indicator(
    #     mode="number",
    #     value=int(sum_total_bikes),
    #     domain={'row': 0, 'column': 1}))
    # fig.update_layout(
    #     grid={'rows': 1, 'columns': 1, 'pattern': "independent"},
    #     template={'data': {'indicator': [{
    #         'title': {'text': f"Total Bikes ({comparison.years_string})"},
    #     }]}}
    # )
