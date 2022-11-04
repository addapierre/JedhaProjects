from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import dash

app = Dash(__name__, use_pages=True)

app.layout = \
html.Div([
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
                    dbc.DropdownMenuItem("Item 1"),
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
    
	dash.page_container
])



@app.callback(
    Output("download-cv", "data"), 
    [Input("cv_btn", "n_clicks")],
    prevent_initial_call=True
)
def dl_cv(_):
    return dcc.send_file('./assets/images.uber_logo.png')

if __name__ == '__main__':
	app.run_server(debug=True)