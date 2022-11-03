import pandas as pd
import numpy as np
import time
import yaml
import requests

from dash import html, Dash, no_update
from dash import dcc
from dash.dependencies import State, Input, Output

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import plotly.express as px
import plotly.graph_objects as go



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


def make_secrets():
    with open('secrets.yaml', 'r') as tt:
        secrets = yaml.full_load(tt)
    return secrets

start_time = time.time()


def init_fig_elbow(dim1, dim2):
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.update_xaxes(autorange = False, range = [dim1,dim2])
    fig1.update_yaxes(autorange=False, range=[0, 1.1], secondary_y = False)
    fig1.update_yaxes(autorange=False, range=[0, 1.1], secondary_y = True)
    fig1.update_layout(
        title="Elbow",
        xaxis_title="Number of clusters")
    fig1.update_yaxes(title_text = "elbow normalized", secondary_y = False)
    fig1.update_yaxes(title_text = "elbow derivative", secondary_y = True)

    return fig1

def init_fig_sil(dim1, dim2):
    fig1 = go.Figure()
    fig1.update_xaxes(autorange = False, range = [dim1,dim2])
    fig1.update_yaxes(autorange=False, range=[0, 1.1])
    fig1.update_layout(
        title="Silhouette",
        xaxis_title="Number of clusters",
        yaxis_title="silhouette")

    return fig1

def init_fig_map():
    fig1 = px.scatter_mapbox(lat=[0],
                            lon=[0],
                            center={'lon': -73.8724, 'lat': 40.7739},
                            mapbox_style='carto-positron',
                            zoom=9,
                            width = 850,
                            height = 1000
                            )

    return fig1


###################################################################################################################################################################################################
###################################################################################################################################################################################################


app.layout = html.Div([

    dcc.Store(
        id = "date", 
        data = {
            'mois' : 1, 
            'jour' : 0, 
            'heure_1' : 10, 
            'heure_2' : 11,
            'liste_mois' :  ['May', 'June', 'July', 'August'],
            'liste_jours' : ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saterday', 'Sunday']
            }),
   
    html.Div([
        html.Div(
            html.H1('NYC Uber requests clustering '), 
            style = {
                'background-color': 'white',
                'height': '50px',
                'width': '100%',
                'margin-top': '0px',
                'margin-bottom': '20px',
                'padding': '0px',
            }),
        html.Div([
            dcc.Dropdown(
                id = 'month_select',
                options = [{ 'label' : j, 'value' : i} for i, j in enumerate(['May', 'June', 'July', 'August'])],
                value = 0
            ),
            dcc.RadioItems(
                id = 'day_select',
                options = [{'label' : j, 'value' : i} for i, j in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saterday', 'Sunday'])],
                value = 0,
                labelStyle={'display': 'inline-block', 'marginTop': '15px'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}
        ),
        html.Div([
            html.P(id = 'output1'),
            html.P(id = 'output2'),
            html.P(id = 'output3')
        ],
            style={'width': '49%', 'float': 'right', 'display': 'inline-block'}
            )
    ]),
    html.Div([
        dcc.RangeSlider(
            id = 'hour_select',
            min = 0,
            max = 23,
            step = 1,
            value = [10,10],
            tooltip = {"placement" : "bottom", 'always_visible' : True},
            allowCross = False
        )],style={'width': '60%', 'display': 'inline-block'}
    ),
    html.Div([
        html.Button('Submit', className = 'button' ,id='submit-val', n_clicks=0 )],
     style={'width': '39%', 'float': 'right', 'display': 'inline-block'}
    ),
    html.Div([
        dcc.Graph(id = 'elbow', figure=init_fig_elbow(0,12), ),
        dcc.Graph(id = 'silhouette', figure=init_fig_sil(0,16))

    ],
    style={'width': '49%', 'display': 'inline-block'}
    ),
    html.Div([
        dcc.Graph(id = 'NY_map', figure = init_fig_map())
    ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})

])


###################################################################################################################################################################################################
###################################################################################################################################################################################################



                                            #UPDATE DE LA VARIABLE DATE
@app.callback(
        [
            Output("output1", 'children'), 
            Output("output2", 'children'), 
            Output("output3", 'children'),
            Output("date", "data")
        ],
        [
            Input("day_select", "value"), 
            Input("month_select", "value"), 
            Input("hour_select", "value")
        ],
        State("date", "data")
        )
def update_day(day, month, hours, date):
    mois = date['liste_mois']
    jour = date['liste_jours']
    date['jour'] = day
    date['mois'] = month
    date['heure_1'] = hours[0]
    date['heure_2'] = hours[1]
    return f'Month: {mois[date["mois"]]}',   f'Day: {jour[date["jour"]]}',  f'from {date["heure_1"]}:00 to {date["heure_2"]+1}:00', date



###################################################################################################################################################################################################

                                            #LIT LE BON FICHIER CSV ET SELECTIONNE LE JOUR ET L'HEURE

@app.callback(
    [
        Output('elbow', 'figure'),
        Output('silhouette', 'figure'),
        Output('NY_map', 'figure')
    ],
    Input('submit-val', 'n_clicks'),
    State('date', 'data'),
    prevent_initial_call=True
)
def submit( _, date):
    secrets = make_secrets()
    body = {}
    
    mois = ['Mai', "Juin", 'Juillet', 'Aout']
    mois = mois[date['mois']]

    body['hour1'] = date['heure_1']
    body['hour2'] = date['heure_2']
    body['month'] = mois
    body['day'] = date['jour']
    url = secrets['lambda_url']

    request_result = requests.post(url, json = body)
    request_result = request_result.json()

    elbow = request_result['elbow']
    elbow = np.array(elbow)
    elbow = elbow/elbow.max()
    best_elbow = request_result['best_elbow']
    silhouette = request_result['silhouette']
    best_silhouette = request_result['best_silhouette']
    labels = request_result['labels']
    elbow_d = request_result['elbow_d']
    index = request_result['index']

    # index pointe vers les lignes qui correspondent au jour et au mois
    coord = np.load('docker_lambda/data/'+mois+'.npy', allow_pickle=True)
    coord = coord[index]

    # elbow figure
    fig_elbow = make_subplots(specs=[[{"secondary_y": True}]])
    fig_elbow.add_trace( 
        go.Scatter(
            x = list(range(2,14)),
            y = elbow,
            mode='lines+markers',
            name="Elbow",
            )
        , secondary_y = False )
    fig_elbow.add_trace(
        go.Scatter(
            x = list(range(3,13)), 
            y = elbow_d,
            line=dict(color='#d991ff', dash = 'dash'),
            name = "elbow derivative"
            ), 
        secondary_y = True)
    fig_elbow.update_layout(
        title="Elbow",
        xaxis_title="Number of clusters")
    fig_elbow.update_yaxes(title_text = "elbow normalized", secondary_y = False)
    fig_elbow.update_yaxes(title_text = "elbow derivative", secondary_y = True)
    fig_elbow.add_shape(
        type='line',
        x0=best_elbow, y0=0, x1=best_elbow, y1=1.1,
        line=dict(
            color='Red', dash="dot"
        ))


    # silhouette figure
    silhouette = np.array(silhouette)
    fig_sil = go.Figure()



    fig_sil.add_trace(go.Bar(x=list(range(best_elbow, best_elbow+silhouette.shape[0])), y=silhouette, name='silhouette'))
    fig_sil.update_xaxes(autorange=True, range=[0, 16])
    fig_sil.update_yaxes(autorange=False, range=[silhouette.min()-0.2, silhouette.max()+0.3])
    fig_sil.update_layout(
        title="Silhouette",
        xaxis_title="number of clusters",
        yaxis_title="silhouette")
    fig_sil.add_annotation(
        x = best_silhouette,  # arrows' head
        y = silhouette.max(),  # arrows' head
        ax = best_silhouette,  # arrows' tail
        ay = silhouette.max()+0.2,  # arrows' tail
        xref = 'x',
        yref = 'y',
        axref = 'x',
        ayref = 'y',
        text = '',  # if you want only the arrow
        showarrow = True,
        arrowhead = 3,
        arrowsize = 1.5,
        arrowwidth = 3,
        arrowcolor = 'red'
    )

    # display labeled points on map
    coord_df = pd.DataFrame(coord[:,:2], columns = ['Lat', 'Lon'])
    coord_df['labels'] = labels

    map_fig = px.scatter_mapbox(coord_df,
                            lat = 'Lat' ,
                            lon = 'Lon',
                            color = 'labels',
                            center={'lon': -73.8724, 'lat': 40.7739},
                            mapbox_style='carto-positron',
                            zoom=9,
                            width=850,
                            height=1000
                            )


    return [fig_elbow, fig_sil, map_fig]


if __name__ == '__main__':
    app.run_server(debug=True)

