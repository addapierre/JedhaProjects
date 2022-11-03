from dash import Dash, html, dcc
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
            
            # html.Div(
            #     dcc.Link(
            #         f"{page['name']} - {page['path']}", href=page["relative_path"]
            #     )
            # )
            # for page in dash.page_registry.values()
        ]
    ),
    html.Div(style = {"height": "150px", "width": "100%"}),
	dash.page_container
])

if __name__ == '__main__':
	app.run_server(debug=True)