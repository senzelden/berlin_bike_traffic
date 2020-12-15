"""bike count dashboard in dash"""

import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output

from barchart_helper import (
    Frequency,
    prepare_dataframe,
    get_parts_for_barchart,
    frequency_dict,
    streets_dict,
)
from comparison_helper import ComparisonBetweenStations, prepare_comparison_df, aggregate
from polar_helper import prepare_data_for_polar

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("berlin_bikedata_2017-2019.csv")
prepare_dataframe(df)
barchart_object = Frequency("Week", frequency_dict, "27")
barchart_df, barchart_title = get_parts_for_barchart(df, barchart_object)

comparison_df = df.set_index("timestamp")
comparison = ComparisonBetweenStations([2019], "sum")
agg_comp_df = aggregate(comparison_df, comparison)

# Barchart with Total Bikes by year and bicycle counter
comparison_fig = px.bar(
    agg_comp_df.reset_index(),
    x="total_bikes",
    y="description",
    color="total_bikes",
    orientation="h",
    labels={"total_bikes": "Total Bikes", "description": "Bicycle Counter"},
)
comparison_fig.add_annotation(
    text=f"{comparison.years_string}",
    xref="paper",
    yref="paper",
    x=1,
    y=-0.05,
    showarrow=False,
    opacity=0.1,
    font=dict(family="Arial", size=70, color="black"),
)

barchart_fig = px.bar(
    barchart_df[barchart_df.station_short == barchart_object.location_id],
    x="timestamp",
    y="total_bikes",
    color="description",
    title=barchart_title,
)
barchart_fig.update_traces(hovertemplate=barchart_object.hovertext)

fig = go.Figure()

app.layout = html.Div(
    [
        # First row
        html.Div(
            [
                # Image and Input container left
                html.Div(
                    [
                        html.Img(
                            id="bike image",
                            height="180px",
                            src="assets/undraw_bike_ride_7xit.png",
                            style={
                                "border-radius": "30px",
                                "textAlign": "center",
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "center",
                            },
                        ),
                        html.H3("Filter by:", className="filter"),
                        html.H4("Year:", className="control_label"),
                        dcc.Dropdown(
                            id="year-dropdown",
                            options=[
                                {"label": "2017", "value": "2017"},
                                {"label": "2018", "value": "2018"},
                                {"label": "2019", "value": "2019"},
                            ],
                            clearable=False,
                            multi=True,
                            value=[2019],
                            placeholder="year",
                        ),
                        html.H4("Station:", className="control_label"),
                        dcc.Dropdown(
                            id="station-dropdown",
                            options=[
                                {"label": item, "value": item}
                                for item in df["description"].unique().tolist()
                            ],
                            clearable=False,
                            multi=False,
                            value="Maybachufer",
                            placeholder="station",
                        ),
                        html.H4("Timeframe:", className="control_label"),
                        dcc.Dropdown(
                            id="timeframe-dropdown",
                            options=[
                                {"label": "hour", "value": "hour_str"},
                                {"label": "day", "value": "day_name"},
                                {"label": "month", "value": "month_name"},
                            ],
                            clearable=False,
                            multi=False,
                            value="hour_str",
                            placeholder="timeframe",
                        ),
                        html.H4("Radial Range:", className="control_label"),
                        dcc.Dropdown(
                            id="radialrange-dropdown",
                            options=[
                                {"label": "max", "value": "max"},
                                {"label": "median", "value": "median"},
                            ],
                            clearable=False,
                            multi=False,
                            value="max",
                            placeholder="radial range",
                        ),
                    ],
                    className="pretty-container",
                ),
                # Title and main-graph container right
                html.Div(
                    [
                        html.Div(
                            [
                                html.H1(
                                    "Berlin Bike Traffic (2017-2019)",
                                    style={
                                        "textAlign": "center",
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "center",
                                    },
                                )
                            ],
                            className="pretty-container",
                        ),
                        html.Div(
                            [
                                #
                                html.Iframe(
                                    id="map",
                                    srcDoc=open(
                                        "folium_maps/Maybachufer.html", "r"
                                    ).read(),
                                    width="100%",
                                    height="300",
                                ),
                            ],
                            className="pretty-container",
                        ),
                        html.Div([
                            html.Div(
                                [
                                    dcc.Graph(
                                        id="scatter-polar",
                                        figure=fig,
                                    ),
                                ],
                                className="pretty-container",
                            ),
                            html.Div(
                                [
                                    dcc.Graph(
                                        id="comparison-bar",
                                        figure=comparison_fig,
                                    ),
                                ],
                                className="pretty-container",
                            ),
                        ], className="basic-container",),
                    ],
                    className="basic-container-column twelve columns",
                ),
            ],
            className="basic-container",
        ),
        # Second row
        html.Div(
            [
                # Barchart left
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id="bar-chart",
                                    figure=barchart_fig,
                                ),
                            ],
                            className="pretty-container",
                        ),
                    ],
                    className="basic-container-column twelve columns",
                ),
                # Dropdowns right
                html.Div(
                    [
                        html.H4("Street:", className="control_label"),
                        dcc.Dropdown(
                            id="two-direction-station-dropdown",
                            options=[
                                {"label": key, "value": value}
                                for key, value in streets_dict.items()
                            ],
                            style={
                                "flex-grow": "2",
                            },
                            clearable=False,
                            multi=False,
                            value="21",
                            placeholder="station",
                        ),
                        html.H4("Frequency:", className="control_label"),
                        dcc.Dropdown(
                            id="frequency-dropdown",
                            options=[
                                {"label": "Day", "value": "Day"},
                                {"label": "Week", "value": "Week"},
                                {"label": "Month", "value": "Month"},
                                {"label": "Year", "value": "Year"},
                            ],
                            style={
                                "flex-grow": "2",
                            },
                            clearable=False,
                            multi=False,
                            value="Month",
                            placeholder="frequency",
                        ),
                    ],
                    className="pretty-container three columns",
                ),
            ],
            className="basic-container",
        ),
    ]
)


@app.callback(
    [Output("scatter-polar", "figure"), Output("map", "srcDoc"), Output("comparison-bar", "figure")],
    [
        Input("year-dropdown", "value"),
        Input("station-dropdown", "value"),
        Input("timeframe-dropdown", "value"),
        Input("radialrange-dropdown", "value"),
    ],
)
def update_fig(year, station, timeframe, radialrange):
    """updates polar chart"""
    df = pd.read_csv("berlin_bikedata_2017-2019.csv")
    if year != "year":
        is_year = df["year"].isin(year)
        complete_df = df[is_year]
    else:
        complete_df = df
    if station != "station":
        pass
    else:
        station = "Maybachufer"
    if timeframe != "timeframe":
        pass
    else:
        timeframe = "day_name"
    if radialrange != "radial range":
        pass
    else:
        radialrange = "max"

    CATEGORY = timeframe  # 'hour_str'
    CAT_SORTERS = {"day_name": "weekday", "hour_str": "hour", "month_name": "month"}
    df_median, df_max, radialrange_dict, categories = prepare_data_for_polar(
        complete_df, CATEGORY, CAT_SORTERS, station
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=df_max["total_bikes"],
            theta=categories,
            fill="toself",
            name="max",
            fillcolor="lightgreen",
            mode="markers",
            text=df_max["location"],
            marker_color="lightgreen",
            hovertemplate="<b>%{text}</b><br><i>%{theta}</i><br><br>Max: %{r} bikes<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=df_median["total_bikes"],
            theta=categories,
            fill="toself",
            name="median",
            fillcolor="dodgerblue",
            mode="markers",
            marker_color="dodgerblue",
            text=df_median["location"],
            hovertemplate="<b>%{text}</b><br><i>%{theta}</i><br><br>Median: %{r} bikes<extra></extra>",
        )
    )

    fig.update_layout(
        showlegend=True,
        title=f"Maximum and Median Bikes for {station}",
        polar=dict(
            radialaxis_tickfont_size=10,
            radialaxis=dict(range=[0, radialrange_dict[radialrange]]),
            angularaxis=dict(
                tickfont_size=10,
                rotation=90,  # start position of angular axis
                direction="clockwise",
            ),
        ),
    )
    aggregation_type = "sum"
    x_label = "Total Bikes"
    if radialrange == "median":
        aggregation_type = "mean"
        x_label = "Average Bikes"
    comparison = ComparisonBetweenStations(year, aggregation_type)
    agg_comp_df = aggregate(comparison_df, comparison)

    # Barchart with Total Bikes by year and bicycle counter
    comparison_fig = px.bar(
        agg_comp_df.reset_index(),
        x="total_bikes",
        y="description",
        color="total_bikes",
        orientation="h",
        labels={"total_bikes": x_label, "description": "Bicycle Counter"},
    )
    comparison_fig.add_annotation(
        text=f"{comparison.years_string}",
        xref="paper",
        yref="paper",
        x=1,
        y=-0.05,
        showarrow=False,
        opacity=0.1,
        font=dict(family="Arial", size=70, color="black"),
    )

    return fig, open(f"folium_maps/{station}.html", "r").read(), comparison_fig


@app.callback(
    Output("bar-chart", "figure"),
    [
        Input("two-direction-station-dropdown", "value"),
        Input("frequency-dropdown", "value"),
    ],
)
def update_barchart_fig(street, frequency):
    """updates bar chart"""
    barchart_object = Frequency(frequency, frequency_dict, street)
    barchart_df, barchart_title = get_parts_for_barchart(df, barchart_object)
    barchart_fig = px.bar(
        barchart_df[barchart_df.station_short == barchart_object.location_id],
        x="timestamp",
        y="total_bikes",
        color="description",
        title=barchart_title,
        labels={
            "total_bikes": "Total Bikes",
            "description": "Street",
            "timestamp": f"{frequency}",
        },
    )
    barchart_fig.update_traces(hovertemplate=barchart_object.hovertext)
    barchart_fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        )
    )

    return barchart_fig


if __name__ == "__main__":
    app.run_server(debug=True)
