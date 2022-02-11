import pandas as pd
import numpy as np
import json

import dash
from dash import html, Dash, dcc
#from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform
from dash.dependencies import State , Input, Output
import re

import plotly.express as px
import plotly.graph_objects as go

import plotly.express as px
import plotly.graph_objects as go


app = Dash(__name__)
server = app.server

weather_df = pd.read_csv("meteo_week.csv", 
        usecols = ['Places', 'latitude', 'longitude', 'Tmin', 'Tmax', 'Humidity', 'clouds'], 
        dtype = {x : np.float16 for x in ['latitude', 'longitude', 'Tmin', 'Tmax']} | {x : np.int8 for x in ['Humidity', 'clouds'] } )

avg_weather = weather_df.groupby('Places').mean().reset_index()

avg_weather.Humidity = avg_weather.Humidity.apply(lambda x: (x*-1)+100)
avg_weather.clouds = avg_weather.clouds.apply(lambda x: (x*-1)+100)

booking = pd.read_csv('booking.csv')


def init_fig_map():
    fig1 = px.scatter_mapbox(lat=[0],
                            lon=[0],
                            center={'lon': 2.398782, 'lat': 47.081012},
                            mapbox_style='carto-positron',
                            zoom=5,
                            width = 850,
                            height = 1000
                            )

    return fig1

###################################################################################################################################################################################################
###################################################################################################################################################################################################

app.layout = html.Div([
    html.H1('Plan a trip with Kayak'),
    
    html.Div([ 
        html.B('choose a weather feature upon which the best locations will be calculated'),
        dcc.RadioItems(
                    id = 'weather_select',
                    options = [{"label" : 'Maximum Temperature', "value" : 'Tmax'},
                        {"label" :'Minimum Temperature', "value" : 'Tmin'},
                        {"label" :'Clouds', "value" : 'clouds'},
                        {"label" :'Humidity', "value" : 'Humidity'}
                        ],
                    value = 'Maximum Temperature',
                    labelStyle={'display': 'inline-block', 'marginTop': '15px'}
                ),
        dcc.Graph(id = 'fr_map', figure = init_fig_map())
        ],
        style={'width': '49%', 'float': 'left', 'display': 'inline-block'}
        ),
    html.Div([
            html.H2(id = 'hidden_text'),
            dcc.Dropdown(id = 'loc_select'),
            dcc.Graph(id = 'loc_map', figure = init_fig_map())
            ],
        style={'width': '49%', 'float': 'right', 'display': 'inline-block'}
        )
])

###################################################################################################################################################################################################
###################################################################################################################################################################################################

@app.callback(
        [Output("fr_map", 'figure'),
        Output('hidden_text','children'),
        Output('loc_select','options')],
        Input("weather_select", "value"),
        prevent_initial_call=True)
def update_weather(weather_feature):


    best_weather = avg_weather.sort_values(weather_feature, ascending = False).reset_index(drop = True).iloc[:10,:]
    fig = px.scatter_mapbox(best_weather,
                            lat = 'latitude' ,
                            lon = 'longitude',
                            color = 'Tmax',
                            size = 'clouds',
                            hover_name = 'Places',
                            hover_data = ['Tmin', 'Tmax'],
                            center={'lon': 2.398782, 'lat': 47.081012},
                            mapbox_style='carto-positron',
                            zoom=5,
                            width=850,
                            height=1000
                            )

    options = [{ 'label' : x, 'value' : x} for x in best_weather.Places.values]
    text = 'Choose a city amongst the best location:'
    return fig, text, options

###################################################################################################################################################################################################

@app.callback(
        Output("loc_map", 'figure'),
        Input("loc_select", "value"),
        prevent_initial_call=True)
def update_loc(place):
    hotels = booking.loc[booking.Lieu == place, :].sort_values('Score', ascending = False).reset_index(drop = True).loc[:5,:]


    fig = px.scatter_mapbox(hotels,
                            lat = 'lat' ,
                            lon = 'lon',
                            color = 'Score',
                            hover_name = 'Nom',
                            hover_data = ['Score'],
                            size = 'Score' ,
                            mapbox_style='carto-positron',
                            zoom = 10,
                            width=850,
                            height=1000
                            )

    return fig


###################################################################################################################################################################################################
###################################################################################################################################################################################################


if __name__ == '__main__':
    app.run_server(debug=True)
