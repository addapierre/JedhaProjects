import pandas as pd
import numpy as np
import json
import time

import dash
from dash import html, Dash
from dash import dcc
#from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform
from dash.dependencies import Input, Output, State
import re
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

import plotly.express as px
import plotly.graph_objects as go

import plotly.express as px
import plotly.graph_objects as go



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)#, transforms=[MultiplexerTransform()])
server = app.server

start_time = time.time()
date = {'mois' : 1, 'jour' : 0, 'heure_1' : 10, 'heure_2' : 11}
mois = ['Mai', 'Juin', 'Juillet', 'Aout']
jour = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
foo = 0

def init_fig_elbow(dim1, dim2):
    fig1 = go.Figure()
    fig1.update_xaxes(autorange = False, range = [dim1,dim2])
    fig1.update_yaxes(autorange=False, range=[0, 1.1])
    fig1.update_layout(
        title="Elbow",
        xaxis_title="Number of clusters",
        yaxis_title="elbow normalized")

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

    dcc.Store(id='dataframe_store'),
    dcc.Store(id='elbow_store'),
    dcc.Store(id='best_values_store'),
    dcc.Store(id='intermediate'),

    html.P(id='balise_vide0'), 
    html.P(id='balise_vide1'),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id = 'month_select',
                options = [{ 'label' : j, 'value' : i} for i, j in enumerate(mois)],
                value = 0
            ),
            dcc.RadioItems(
                id = 'day_select',
                options = [{'label' : j, 'value' : i} for i, j in enumerate(jour)],
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
            value = [10,10],
            tooltip = {"placement" : "bottom", 'always_visible' : True},
            allowCross = False
        )],style={'width': '60%', 'display': 'inline-block'}
    ),
    html.Div([
        html.Button('Submit', id='submit-val', n_clicks=0)],
     style={'width': '39%', 'float': 'right', 'display': 'inline-block'}
    ),
    html.Div([
        dcc.Graph(id = 'elbow', figure=init_fig_elbow(0,16)),
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
        [Output("output1", 'children'), Output("output2", 'children'), Output("output3", 'children')],
        [Input("day_select", "value"), Input("month_select", "value"), Input("hour_select", "value")])
def update_day(day, month, hours):
    date['jour'] = day
    date['mois'] = month
    date['heure_1'] = hours[0]
    date['heure_2'] = hours[1]
    return f'mois: {mois[date["mois"]]}',   f'jour: {jour[date["jour"]]}',  f'de {date["heure_1"]}h à {date["heure_2"]+1}h'

###################################################################################################################################################################################################
###################################################################################################################################################################################################

                                            #LIT LE BON FICHIER CSV ET SELECTIONNE LE JOUR ET L'HEURE

@app.callback(
    [Output('dataframe_store', 'data'),
    Output('intermediate', 'data')],
    Input('submit-val', 'n_clicks'),
    prevent_initial_call=True
)
def read_file(n_clicks):

    print(time.time() - start_time)
    #Selection du mois
    filepath = './uber-trip-data/'+mois[date["mois"]]+'.csv'
    full_month =  pd.read_csv(filepath, usecols=['hour', 'dayofweek', 'Lat', 'Lon'], dtype={'hour' : np.int8, 'dayofweek' : np.int8,'Lat' : np.float32, 'Lon' : np.float32 })

    # Selection des heures    

    if date["heure_1"] == date["heure_2"]:
        full_month = full_month.loc[full_month.hour == date["heure_1"], :]
    else:
        full_month = full_month.loc[(full_month.hour >= date["heure_1"] ) & (full_month.hour <= date["heure_2"] ), :]

    # Selection du jour 

    df = full_month.loc[full_month.dayofweek == date["jour"], ['Lat','Lon']].copy()

    intermediate = json.dumps({'kmeans_list' : [], 'i': 0, "elbow" : [], })

    return df.to_json(), intermediate

###################################################################################################################################################################################################
###################################################################################################################################################################################################



                                               #CALCUL DE L'ELBOW
                                               


@app.callback(
    [Output('elbow', 'figure'),
     Output('elbow_store', 'data')],
    Input('dataframe_store', 'data'),
    State('intermediate', 'data'),
    prevent_initial_call=True
)
def elbow1(df, intermediate):

    df = pd.read_json(df, dtype={'Lat' : np.float32, 'Lon' : np.float32 })

    elbow = json.loads(intermediate)['elbow']
    kmeans_list = json.loads(intermediate)['kmeans_list']
    k = []
    best_elbow = 0
    fig_elb = go.Figure()
    X = df[['Lat', 'Lon']].values

     

    for i in (range_elbow := range(1, 15)) :
        print(i, (time.time() - start_time))
        kmeans = KMeans(n_clusters=i, random_state=0)
        kmeans.fit(X)
        kmeans_list.append(kmeans.labels_.tolist())
        elbow.append(kmeans.inertia_)
        k.append(i)
    elbow = np.asarray(elbow)
    elbow = elbow / elbow[0]
    fig_elb.add_trace(go.Scatter(x=list(range_elbow),
                             y=elbow,
                             mode='lines+markers',
                             name='elbow'))
    fig_elb.update_layout(
        title="Elbow",
        xaxis_title="Number of clusters",
        yaxis_title="elbow normalized")
    
    #Approximation du meilleur elbow
    pente = (elbow[-1]-elbow[0])/(range_elbow[-1]-range_elbow[0])
    for i in range_elbow[1:]:
        d_elbow = elbow[i]-elbow[i-1]
        if d_elbow > pente:
            best_elbow = i
            break
    fig_elb.update_xaxes(autorange = False, range = [0,16])
    fig_elb.update_yaxes(autorange=False, range=[0, 1.1])
    fig_elb.add_shape( type='line',
        x0=best_elbow, y0=0, x1=best_elbow, y1=1.1,
        line=dict(
            color='Red', dash="dot"
        ))
    elbow_json = json.dumps({'kmeans_list' : kmeans_list, 'best_elbow': best_elbow})
    
    return [fig_elb, elbow_json]

###################################################################################################################################################################################################
###################################################################################################################################################################################################


                                        #CALCUL DE LA SILHOUETTE
@app.callback(
    [Output('silhouette', 'figure'),
     Output('best_values_store', 'data')],
    Input('elbow_store', 'data'),
    State('dataframe_store', 'data'),
    prevent_initial_call=True
)
def silhouette(elbow_json, df):
    kmeans_list, best_elbow  = json.loads(elbow_json)['kmeans_list'], json.loads(elbow_json)['best_elbow']
    df = pd.read_json(df, dtype={'Lat' : np.float32, 'Lon' : np.float32 })
    X = np.asarray(df[['Lat', 'Lon']])

    ##global best_sil, best_kmeans
    sil = []
    k = []
    fig_sil = go.Figure()

    if best_elbow + 6 < 15:
        for i in range(best_elbow, best_elbow + 6):
            sil.append(silhouette_score(X, kmeans_list[i]))
            k.append(i)
    else:
        for i in range(best_elbow, 15):
            sil.append(silhouette_score(X, kmeans_list[i]))
            k.append(i)
    sil = np.asarray(sil)
    best_sil = k[sil.argsort()[-1]]
    best_kmeans = kmeans_list[best_sil]

    fig_sil.add_trace(go.Bar(x=k, y=sil, name='silhouette'))
    fig_sil.update_xaxes(autorange=True, range=[0, 16])
    fig_sil.update_yaxes(autorange=False, range=[sil[sil.argsort()[0]]-0.2, sil[sil.argsort()[-1]]+0.3])
    fig_sil.update_layout(
        title="Silhouette",
        xaxis_title="number of clusters",
        yaxis_title="silhouette")
    fig_sil.add_annotation(
        x=best_sil,  # arrows' head
        y=sil[sil.argsort()[-1]],  # arrows' head
        ax=best_sil,  # arrows' tail
        ay=sil[sil.argsort()[-1]]+0.2,  # arrows' tail
        xref='x',
        yref='y',
        axref='x',
        ayref='y',
        text='',  # if you want only the arrow
        showarrow=True,
        arrowhead=3,
        arrowsize=1.5,
        arrowwidth=3,
        arrowcolor='red'
    )
    best_json = json.dumps({'best_sil' : best_sil, 'best_kmeans' : best_kmeans})

    return fig_sil, best_json

###################################################################################################################################################################################################
###################################################################################################################################################################################################


                                                #AFFICHAGE DE LA CARTE
@app.callback(
    Output('NY_map', 'figure'),
    Input('best_values_store', 'data'),
    State('dataframe_store', 'data'),
    prevent_initial_call=True
)
def map_NYC(best_json, df):
    df = pd.read_json(df, dtype={'Lat' : np.float32, 'Lon' : np.float32 })
    best_kmeans = json.loads(best_json)['best_kmeans']

    df['labels']= best_kmeans
    fig = px.scatter_mapbox(df,
                            lat = 'Lat' ,
                            lon = 'Lon',
                            color = 'labels',
                            center={'lon': -73.8724, 'lat': 40.7739},
                            mapbox_style='carto-positron',
                            zoom=9,
                            width=850,
                            height=1000
                            )

    return fig

###################################################################################################################################################################################################
###################################################################################################################################################################################################


if __name__ == '__main__':
    app.run_server(debug=True)

