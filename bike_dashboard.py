import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('berlin_bikedata_2017-2019.csv')

fig = go.Figure()

app.layout = html.Div([
    # First row
    html.Div([

        # Image and Input container left
        html.Div([
            html.Img(id="bike image",
                     height="180px",
                     src="assets/undraw_bike_ride_7xit.png",
                     style={"border-radius": "30px",
                            "textAlign": "center",
                            "display":"flex",
                            "alignItems":"center",
                            "justifyContent": "center"}),

            html.H3("Filter by:",
                    className="filter"),

            html.H4("Year:",
                    className="control_label"),

            dcc.Dropdown(
                id='year-dropdown',
                options=[
                    {'label': '2017', 'value': '2017'},
                    {'label': '2018', 'value': '2018'},
                    {'label': '2019', 'value': '2019'}
                ],
                clearable=False,
                multi=True,
                value=[2019],
                placeholder="year",
            ),

            html.H4("Station:",
                    className="control_label"),

            dcc.Dropdown(
                id='station-dropdown',
                options=[{'label': item, 'value': item} for item in df['description'].unique().tolist()],
                clearable=False,
                multi=False,
                value="Maybachufer",
                placeholder="station",
            ),

            html.H4("Timeframe:",
                    className="control_label"),

            dcc.Dropdown(
                id='timeframe-dropdown',
                options=[
                    {'label': 'hour', 'value': 'hour_str'},
                    {'label': 'day', 'value': 'day_name'},
                    {'label': 'month', 'value': 'month_name'}
                ],
                clearable=False,
                multi=False,
                value="hour_str",
                placeholder="timeframe",
            ),

            html.H4("Radial Range:",
                    className="control_label"),

            dcc.Dropdown(
                id='radialrange-dropdown',
                options=[
                    {'label': 'max', 'value': 'max'},
                    {'label': 'median', 'value': 'median'}
                ],
                clearable=False,
                multi=False,
                value="max",
                placeholder="radial range",
            ),
        ], className="pretty-container"),
        # Title and main-graph container right
        html.Div([
            html.Div([
                html.H1('Berlin Bike Traffic (2017-2019)',
                        style={"textAlign": "center",
                               "display":"flex",
                               "alignItems":"center",
                               "justifyContent": "center"})
            ], className="pretty-container"),
            html.Div([
                #
                html.Iframe(id='map', srcDoc=open('folium_maps/Maybachufer.html', 'r').read(), width='100%', height='300'),
            ], className="pretty-container"),
            html.Div([
                dcc.Graph(
                    id='scatter-polar',
                    figure=fig,
                ),
            ], className="pretty-container"),


        ], className="basic-container-column twelve columns"),
    ], className="basic-container"),

    # Second row
    html.Div([
        # Barchart left
        html.Div([
            # To Do: Implement Bar chart
        ], className="pretty-container"),
        # Dropdowns right
        html.Div([
            # To Do: Implement Dropdowns
        ], className="pretty-container"),
    ], className="basic-container"))
])


@app.callback(
    [Output('scatter-polar', 'figure'),
     Output('map', 'srcDoc')],
    [
     Input('year-dropdown', 'value'),
     Input('station-dropdown', 'value'),
     Input('timeframe-dropdown', 'value'),
     Input('radialrange-dropdown', 'value')
    ]
)
def update_fig(year, station, timeframe, radialrange):
    df = pd.read_csv('berlin_bikedata_2017-2019.csv')
    if year != "year":
        is_year = df['year'].isin(year)
        complete_df = df[is_year]
    else:
        complete_df = df
    if station != "station":
        pass
    else:
        station = 'Maybachufer'
    if timeframe != "timeframe":
        pass
    else:
        timeframe = 'day_name'
    if radialrange != "radial range":
        pass
    else:
        radialrange = 'max'

    CATEGORY = timeframe  # 'hour_str'
    CAT_SORTERS = {'day_name': 'weekday', 'hour_str': 'hour', 'month_name': 'month'}

    df_median = complete_df[(complete_df.description == station)].groupby([CATEGORY, CAT_SORTERS[CATEGORY]])[
        ['total_bikes']].median().reset_index().sort_values(CAT_SORTERS[CATEGORY])
    df_median['location'] = station
    df_max = complete_df[(complete_df.description == station)].groupby([CATEGORY, CAT_SORTERS[CATEGORY]])[
        ['total_bikes']].max().reset_index().sort_values(CAT_SORTERS[CATEGORY])
    df_max['location'] = station
    radialrange_dict = {'max': df_max['total_bikes'].max(), 'median': df_median['total_bikes'].max()}

    categories = df_median[CATEGORY]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=df_max['total_bikes'],
        theta=categories,
        fill='toself',
        name='max',
        fillcolor="lightgreen",
        mode='markers',
        text=df_max['location'],
        marker_color='lightgreen',
        hovertemplate="<b>%{text}</b><br><i>%{theta}</i><br><br>Max: %{r} bikes<extra></extra>",

    ))

    fig.add_trace(go.Scatterpolar(
        r=df_median['total_bikes'],
        theta=categories,
        fill='toself',
        name='median',
        fillcolor="dodgerblue",
        mode='markers',
        marker_color='dodgerblue',
        text=df_median['location'],
        hovertemplate="<b>%{text}</b><br><i>%{theta}</i><br><br>Median: %{r} bikes<extra></extra>"
    ))

    fig.update_layout(
        showlegend=False,
        polar=dict(
            radialaxis_tickfont_size=10,
            radialaxis=dict(range=[0, radialrange_dict[radialrange]]),
            angularaxis=dict(
                tickfont_size=10,
                rotation=90,  # start position of angular axis
                direction="clockwise"
            )
        )
    )

    return fig, open(f'folium_maps/{station}.html', 'r').read()


if __name__ == '__main__':
    app.run_server(debug=True)