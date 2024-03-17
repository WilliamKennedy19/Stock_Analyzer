"""
Author: William Kennedy

"""
import yfinance as yf
import pandas as pd
import dash
from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc

dash.register_page(__name__)

class statements:
    def __init__(self, initial_ticker:str = "META"):
        pass

    def create_layout():
        layout = html.Div([])