from dash import html, dcc


layout = \
    html.Div(
        children = \
        [
            html.Div([
                html.H1( "Projects for Jedha Data Science bootcamp.", 
                    style = {
                        "float": "left",
                        'margin-left': '30vw'}),
                html.A(
                    html.Img(src='assets/images/jedha_logo.png', className='logo'), 
                    href="https://en.jedha.co/", 
                    style= {
                        'margin-top': '-15px',
                        "float": "left"})
                ], 
                style = {
                    'width' : '100%',
                    "text-align": "center"
                }),
            html.Div(
                className="table",
                children = [
                    html.Div(
                    className='tr',
                    children = 
                    [
                        html.Div(className='tcell',
                        children= html.Div( className='project-block',
                            children = 
                            [
                                html.Div
                                ( 
                                    className= 'subhead',
                                    children = html.A(
                                            children=\
                                            [
                                                html.Img(
                                                    src='assets/images/uber_logo.png',
                                                    style= {
                                                        "float": "left",
                                                        "height": "60px",
                                                        "width": "60px",
                                                        'margin-left': '20px',
                                                        'margin-top': '5px'
                                                    }),
                                                dcc.Markdown(
                                                    """### Uber Hot Spots in New-York""",
                                                    style = {
                                                        'transform' : 'translate(-1%, 5%)'
                                                    }
                                                    ),
                                            ],
                                            className='titre-projet',
                                            href='/apps/uber_project',
                                            style = {
                                                "text-align": "center",
                                                }
                                        ),
                                ),
                                dcc.Markdown(
                                    """
                                    ### Objectives:

                                    - With NYC uber logs (timestamp and coordinates), use **clustering** algorithms to get hot-spots for specific time windows
                                    
                                    ### Methods:

                                    - **ETL/EDA**: *Pandas* and *Numpy*
                                    - **Clustering**: *scikit-learn* K-Means, automated elbow method
                                    - **Deployment**: *Dash*, *Heroku*, and *AWS Lambda*

                                    ### App: 
                                    """,
                                    style = {
                                        "margin": "20px"
                                    }
                                ),
                                html.A(
                                    html.Img(
                                        src = 'assets/images/uber_app.png',
                                        style = {
                                            "width" : "auto",
                                            "height" : "auto",
                                            "max-width" : "270px",
                                            "margin-top" : "-50px",
                                            "margin-left": "100px",
                                            "box-shadow": "0px 0px 10px grey"
                                        }
                                    ),
                                    href = "https://uber-clustering.herokuapp.com/"
                                )
                                
                            ]
                        )),
                        html.Div(className='tcell',
                        children= html.Div( className='project-block',
                            children = 
                            [
                                html.Div( className= 'subhead',
                                    children = html.A(
                                        children=\
                                            [
                                                html.Img(
                                                    src='assets/images/booking_logo.png',
                                                    style= {
                                                        "float": "left",
                                                        "height": "60px",
                                                        "width": "60px",
                                                        'margin-left': '20px',
                                                        'margin-top': '5px'
                                                    }),
                                                dcc.Markdown(
                                                    """### Plan your trip with Booking.com""",
                                                    style = {
                                                        'transform' : 'translate(-1%, 5%)'
                                                    }
                                                    ),
                                            ],
                                            className='titre-projet',
                                            href='www.google.com',
                                            style = {
                                                "text-align": "center",
                                                }
                                    )),
                                dcc.Markdown(
                                    """
                                    ### Objectives:

                                    - Use an API to get next week's weather forecast.
                                    - Scrape booking.com to get touristic location's hotel info (gps coord., ratings, desc.)
                                    - Make an app to select the best destination and hotel for your vacations.
                                    
                                    ### Methods:

                                    - **ETL/EDA**: *API* with requests library, *Pandas* 
                                    - **Scraping**: scraping booking.com with *scrapy*
                                    - **Deployment**: *Dash* and *Heroku*

                                    ### App: 
                                    """,
                                    style = {
                                        "margin": "20px"
                                    }
                                ),
                                html.A(
                                    html.Img(
                                        src = 'assets/images/kayak_app.png',
                                        style = {
                                            "width" : "auto",
                                            "height" : "auto",
                                            "max-width" : "270px",
                                            "margin-top" : "-50px",
                                            "margin-left": "100px",
                                            "box-shadow": "0px 0px 10px grey"
                                        }
                                    ),
                                    href = "https://kayak-app-pierre.herokuapp.com/"
                                )
                                
                            ]
                        )),
                        html.Div(className='tcell',
                        children= html.Div( className='project-block',
                            children = 
                            [
                                html.Div( className= 'subhead',
                                    children = html.A(
                                        children=\
                                            [
                                                html.Img(
                                                    src='assets/images/walmart_logo.png',
                                                    style= {
                                                        "float": "left",
                                                        "height": "60px",
                                                        "width": "60px",
                                                        'margin-left': '20px',
                                                        'margin-top': '5px'
                                                    }),
                                                dcc.Markdown(
                                                    """### Walmart sales predictions.""",
                                                    style = {
                                                        'transform' : 'translate(-1%, 5%)'
                                                    }
                                                    ),
                                            ],
                                            className='titre-projet',
                                            href='https://github.com/addapierre/JedhaProjects/tree/main/Walmart',
                                            style = {
                                                "text-align": "center",
                                                }
                                    )),
                                dcc.Markdown(
                                    """
                                    ### Objectives:

                                    - Clean a walmart sales dataset.
                                    - impute missing data.
                                    - Use regression models with regulation to predict a store sales.
                                    
                                    ### Methods:

                                    - **ETL/EDA**: *Pandas* 
                                    - **ML**: *scikit-learn* ridge and lasso regression, grid search to find best hyperparameters
                                     
                                    """,
                                    style = {
                                        "margin": "20px"
                                    }
                                ),
                                html.A(
                                    dcc.Markdown(
                                        """### Notebook""",
                                        style = {
                                        "margin": "20px"
                                        }
                                    ),
                                    className='titre-projet',
                                    href = "https://github.com/addapierre/JedhaProjects/blob/main/Walmart/01-Walmart_sales.ipynb"
                                )
                                
                            ]
                        )),
                        
                    ]
                ),
                html.Div(
                    className='tr',
                    children = 
                    [
                        html.Div(className='tcell',
                        children= html.Div( className='project-block',
                            children = 
                            [
                                html.Div
                                ( 
                                    className= 'subhead',
                                    children = html.A(
                                            children=\
                                            [
                                                html.Img(
                                                    src='assets/images/wine_logo.png',
                                                    style= {
                                                        "float": "left",
                                                        "height": "60px",
                                                        "width": "auto",
                                                        'margin-left': '30px',
                                                        'margin-top': '5px'
                                                    }),
                                                dcc.Markdown(
                                                    """### Wine-O-Meter Flask web page""",
                                                    style = {
                                                        'transform' : 'translate(-1%, 5%)'
                                                    }
                                                    ),
                                            ],
                                            className='titre-projet',
                                            href='https://github.com/addapierre/JedhaProjects/tree/main/Wine-o-meter',
                                            style = {
                                                "text-align": "center",
                                                }
                                        )
                                ),
                                dcc.Markdown(
                                    """
                                    ### Objectives:

                                    - Serve a simple ML model with a Flask  multi-page web app and API
                                    
                                    ### Methods:

                                    - **Deployment**: *Flask* and *Heroku*

                                    ### App: 
                                    """,
                                    style = {
                                        "margin": "20px"
                                    }
                                ),
                                html.A(
                                    html.Img(
                                        src = 'assets/images/wine_app.png',
                                        style = {
                                            "width" : "auto",
                                            "height" : "auto",
                                            "max-width" : "270px",
                                            "margin-top" : "-0px",
                                            "margin-left": "100px",
                                            "box-shadow": "0px 0px 10px grey"
                                        }
                                    ),
                                    href = "https://wine-o-meter-pierre.herokuapp.com/"
                                )
                                
                            ]
                        )),
                        
                    ]
                )],
                style = {
                    'margin': 'auto'
                }
                )
        ]
    )

    