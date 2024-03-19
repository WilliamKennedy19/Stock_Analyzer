"""
Author: William Kennedy
Contributors: Rielly Young

"""
import yfinance as yf
import pandas as pd
from dash import Dash,dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
import pages.statements as statements
import pages.stock_info as stock

# Error onload:
# pandas.errors.UndefinedVariableError: name 'Dividends' is not defined
#
# Reproduction steps:
#   1. remove line 80 
#   1. run main.py
#
# Comments:
# - This error is related to the empty request that is send when the searchbar is empty.
# - You can also remove the ticker from the searchbar without removing line 80 to repro this error.
# - there is def a better way to handle this error.

app = Dash(__name__, external_stylesheets=['assets/style.css'],use_pages=True)


app.layout = html.Div([
    html.Div([
        html.Ul([
            html.Li([
                html.Button(["Stock Information"])
            ]),
            html.Li([
                html.Button("Home", className="dropbtn"),
                html.Div([
                    html.A("Stock Information", href="/"),
                        html.A("Statements",href="pages/statements"),
                        html.A("Fundamental Analysis"),
                        html.A("Technical Analysis"),
                    ],
                    className="dropdown-content",
                    ),
                ],
                className="dropdown",
                ),
            html.Li([
                html.Div([
                    html.Button(
                        [html.I(className="fas fa-search")],
                        id="search",
                        className="btn-search",
                        n_clicks=0,
                        ),
                        dcc.Input(
                            id="input-1-state",
                            className="input-search",
                            type="text",
                            placeholder="input stock ticker...",
                            value="META"
                        ),
                ],
                className="search-box",
                ),
            ]),
        ],
        className="navbar",
        )
    ]
    ),
])


if __name__ == "__main__":
    ticker = yf.Ticker("META")

    app.run(debug=True)

    Stock = stock(ticker)

    app.layout= Stock.layout()

    