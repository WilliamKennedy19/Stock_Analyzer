"""
Author: William Kennedy

"""
import yfinance as yf
import pandas as pd
import dash
from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc



class Statements:
    def __init__(self, initial_ticker:str = "META"):
        self.layout = self.create_layout()
        dash.register_page(__name__)

    def create_layout():
        layout = html.Div([html.H1("Hello World")])

    def run(self, debug=False):
        self.app.run_server(debug=debug)
