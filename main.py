import yfinance as yf
import pandas as pd
import dash
from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc

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


class StockAnalyzerApp:
    def __init__(self, initial_ticker:str = "META"):
        self.app = dash.Dash(__name__, external_stylesheets=['assets/style.css'])
        self.initial_ticker = initial_ticker
        self.initial_stock = yf.Ticker(self.initial_ticker)
        self.initial_stock_hist = self.initial_stock.history().reset_index()
        self.initial_data = (
            self.initial_stock_hist.query("Dividends==0")
            .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
            .sort_values(by="Date")
        )
        self.figure={
                        "data": [
                            {
                                "x": self.initial_data["Date"],
                                "y": self.initial_data["Close"],
                                "type": "scatter",
                                "mode": "lines",
                                "name": "Close Price",
                            }
                        ],
                        "layout": {"title": f"{self.initial_stock.info['shortName']} ({self.initial_ticker}) - Daily Price Changes"},
                    }
        self.app.layout = self.build_layout()
        self.register_callbacks()
    
    def build_layout(self):
        layout = html.Div(
            children=[
                html.Div(
                    [
                        html.Ul(
                            [
                                html.Li(
                                    [
                                        html.Button("Home", className="dropbtn"),
                                        html.Div(
                                            [
                                                html.A("Stock Information", href="/"),
                                                html.A("Statements"),
                                                html.A("Fundamental Analysis"),
                                                html.A("Technical Analysis"),
                                            ],
                                            className="dropdown-content",
                                        ),
                                    ],
                                    className="dropdown",
                                ),
                                html.Li(
                                    [
                                        html.Div(
                                            [
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
                                    ]
                                ),
                            ],
                            className="navbar",
                        )
                    ]
                ),
                html.H1(children="Stock Analyzer Tool"),
                html.H2(
                    children=("Analyzing the price behavior of the stock"),
                    className="chart-header",
                ),
                dcc.Graph(
                    id="stock-chart",
                    figure= self.figure,
                ),
                html.Div(
                    children=[
                html.Table([
                    html.Tr([
                        html.Th([
                            "Operating Cash Flow"
                        ]),
                        html.Th([
                            "P/E Ratio"
                        ]),
                        html.Th([
                            "Enterprise Value"
                        ]),
                        html.Th([
                            "Gross Margins"
                        ]),
                        html.Th([
                            "EPS"
                        ]),
                        html.Th([
                            "Market Capitalization"
                        ]),
                        html.Th([
                            "Revenue Growth"
                        ]),
                        html.Th([
                            "52 Week High"
                        ])

                    ]),

                    html.Tr([
                        html.Td([
                            self.initial_stock.info['operatingCashflow']
                        ],id="opCashFlow"),
                        html.Td([
                            round(self.initial_stock.info['trailingPE'],2)
                        ],id="pe"),
                        html.Td([
                            self.initial_stock.info['enterpriseValue']
                        ],id="enterprise"),
                        html.Td([
                            str(round(self.initial_stock.info['grossMargins']*100,2))+"%"
                        ],id="grossmargins"),
                        html.Td([
                            round(self.initial_stock.info['trailingEps'],2)
                        ],id="eps"),
                        html.Td([
                            self.initial_stock.info['marketCap']
                        ],id="market_cap"),
                        html.Td([
                            self.initial_stock.info['revenueGrowth']
                        ],id="revGrowth"),                    
                        html.Td([
                            self.initial_stock.info['fiftyTwoWeekHigh']
                        ],id="52weekHigh")
                    ]),

                    html.Tr([
                        html.Th([
                            "Free Cash Flow"
                        ]),
                        html.Th([
                            "Return on Assets"
                        ]),
                        html.Th([
                            "Total Debt"
                        ]),
                        html.Th([
                            "EBITDA"
                        ]),
                        html.Th([
                            "Number of Oustanding Shares"
                        ]),
                        html.Th([
                            "Dividend Yield"
                        ]),
                        html.Th([  
                            "Dividend Rate"
                        ]),
                        html.Th([
                            "52 Week Change"
                        ])
                    ]),
                    html.Tr([
                        html.Td([
                            self.initial_stock.info['freeCashflow']
                        ]),
                        html.Td([
                            self.initial_stock.info['returnOnAssets']
                        ]),
                        html.Td([
                            self.initial_stock.info['totalDebt']
                        ]),
                        html.Td([
                            self.initial_stock.info['ebitda']
                        ]),
                        html.Td([
                            self.initial_stock.info['sharesOutstanding']
                        ]),
                        html.Td([
                            self.initial_stock.info['dividendYield']
                        ]),
                        html.Td([
                            self.initial_stock.info['dividendRate']
                        ]),                    
                        html.Td([
                            self.initial_stock.info['52WeekChange']
                        ])
                    ]),
                ], className='styled-table')
            ]
                ),
            ]
        )
        return layout

    def register_callbacks(self):
        @self.app.callback(
            [
                Output(component_id="opCashFlow", component_property="children"),
                Output(component_id="pe", component_property="children"),
                Output(component_id="enterprise", component_property="children"),
                Output(component_id="grossmargins", component_property="children"),
                Output(component_id="eps", component_property="children"),
                Output(component_id="market_cap", component_property="children"),
                Output(component_id="revGrowth", component_property="children"),
                Output(component_id="52weekHigh", component_property="children"),
                Output(component_id="stock-chart", component_property="figure"),
            ],
            [Input("search", "n_clicks")],
            [State("input-1-state", "value")]
            
        )
        def search_ticker(n_clicks, ticker:str= "META"):
            stock = yf.Ticker(str(ticker))
            stock_hist = stock.history().reset_index()
            data = (
                stock_hist.query("Dividends==0.0")
                .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
                .sort_values(by="Date")
            )
            stock_info = stock.info
            opCashFlow = stock_info.get("operatingCashflow")
            pe = round(stock_info.get("trailingPE"), 2)
            enterprise = stock_info.get("enterpriseValue")
            grossmargins = str(round(stock_info.get("grossMargins") * 100, 2)) + "%"
            eps = round(stock_info.get("trailingEps"), 2)
            market_cap = stock_info.get("marketCap")
            revGrowth = stock_info.get("revenueGrowth")
            fiftyTwoWeekHigh = stock_info.get("fiftyTwoWeekHigh")

            self.figure = {
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["Close"],
                        "type": "scatter",
                        "mode": "lines",
                        "name": "Close Price",
                    }
                ],
                "layout": {"title": f"{stock.info['shortName']} ({ticker}) - Daily Price Changes"}
            }

            return (
                opCashFlow,
                pe,
                enterprise,
                grossmargins,
                eps,
                market_cap,
                revGrowth,
                fiftyTwoWeekHigh,
                self.figure
            )

    def run(self, debug=False):
        self.app.run_server(debug=debug)

if __name__ == "__main__":
    StockAnalyzerApp().run(debug=True)
