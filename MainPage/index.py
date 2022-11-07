from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

from app import server
from app import app
from apps import home, uber_project


app.layout = \
html.Div([
    dcc.Location(id='app_url', refresh=False),
    html.Div(
        className='head',
        children = [
            html.A(
                html.H1(
                    'Pierre Adda', 
                    style={
                        "float":"left", 
                        "margin-left": "140px",
                        "margin-right": "100px",
                        "margin-top" : "20px",
                        "font-size" : "3em"
                    }),
                    href="/",
                    style={'color': 'black'}
                ),
            html.A(
                html.Img(src='assets/images/github_logo.png', className='logo'),
                href="https://github.com/addapierre",
                style = {
                    'float' : 'left'
                }
            ),
            html.A(
                html.Img(src='assets/images/linkedin_logo.png', className='logo'),
                href="https://github.com/addapierre",
                style = {
                    'float' : 'left'
                }
            ),
            html.A(
                html.Img(src='assets/images/gmail_logo.png', className='logo'),
                href="mailto:addapierr@gmail.com",
                style = {
                    'float' : 'left'
                }
            ),
            dbc.DropdownMenu(
                label="Menu",
                children=[
                    dbc.DropdownMenuItem("home", href='/apps/home'),
                    dbc.DropdownMenuItem("Item 2"),
                    dbc.DropdownMenuItem("C.V.", id='cv_btn'),
                ],
                menu_variant="dark",
                style = {
                    'float' : 'right',
                    'margin-top' : '20px',
                    'margin-right' : '70px'
                }

            ),
            dcc.Download(id = 'download-cv'),
            
        ]
    ),
    html.Div(style = {"height": "150px", "width": "100%"}),
    html.Div(id='page-content', children=[])
])



@app.callback(
    Output("download-cv", "data"), 
    [Input("cv_btn", "n_clicks")],
    prevent_initial_call=True
)
def dl_cv(_):
    return dcc.send_file('./assets/images.uber_logo.png')


@app.callback(Output('page-content', 'children'),
              [Input('app_url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/home':
        return home.layout
    if pathname == '/apps/uber_project':
        return uber_project.layout
    else:
        return home.layout

if __name__ == '__main__':
	app.run_server(debug=True)