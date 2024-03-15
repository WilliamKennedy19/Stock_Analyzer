import yfinance as YF
from dash import Dash,dcc,html, callback, clientside_callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import json

stock = YF.Ticker("META")
stock_hist = YF.Ticker("META").history().reset_index()

data = (

    stock_hist.query("Dividends==0.0").assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d")).sort_values(by="Date")

)

app = Dash(__name__,external_stylesheets=['venv/assets/style.css'])

# Main app layout for the Stock Information Screen
app.layout = html.Div(

    

    children=[
        html.Div([
            html.Ul([
                html.Li([
                    html.Button("Home",className="dropbtn"),
                    html.Div([
                        html.A("Stock Information",href="/"),
                        html.A("Statements"),
                        html.A("Fundamental Analysis"),
                        html.A("Technical Analysis")
                    ],className="dropdown-content")],
                    className="dropdown"),
                html.Li([
                    html.Div([
                        html.Button([html.I(className="fas fa-search")], id="search",className='btn-search', n_clicks=0),
                        dcc.Input(id="input-1-state",className='input-search', type='text', placeholder='Enter search query...')
                    ],className="search-box"),
                ])
            ],className="navbar")
        ]),

        html.H1(children="Stock Analyzer Tool"),

        html.H2(children=("Analyzing the price behaviour of the stock"),className='chart-header'),

        

        dcc.Graph(id="stock-chart",

            figure={

                "data": [

                    {

                        "x": data["Date"],

                        "y": data["Close"],

                    },

                ],

                "layout": {"title": "Meta Ticker- Daily Price Changes"},

            },

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
                        ]),
                        html.Th([
                            ""
                        ]),

                    ]),

                    html.Tr([
                        html.Td([
                            stock.info['operatingCashflow']
                        ],id="opCashFlow"),
                        html.Td([
                            round(stock.info['trailingPE'],2)
                        ],id="pe"),
                        html.Td([
                            stock.info['enterpriseValue']
                        ],id="enterprise"),
                        html.Td([
                            str(round(stock.info['grossMargins']*100,2))+"%"
                        ],id="grossmargins"),
                        html.Td([
                            round(stock.info['trailingEps'],2)
                        ],id="eps"),
                        html.Td([
                            stock.info['marketCap']
                        ],id="market_cap"),
                        html.Td([
                            stock.info['revenueGrowth']
                        ],id="revGrowth"),                    
                        html.Td([
                            stock.info['fiftyTwoWeekHigh']
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
                        ]),
                        html.Th([
                            
                        ])
                    ]),
                    html.Tr([
                        html.Td([
                            stock.info['freeCashflow']
                        ]),
                        html.Td([
                            stock.info['returnOnAssets']
                        ]),
                        html.Td([
                            stock.info['totalDebt']
                        ]),
                        html.Td([
                            stock.info['ebitda']
                        ]),
                        html.Td([
                            stock.info['sharesOutstanding']
                        ]),
                        html.Td([
                            stock.info['dividendYield']
                        ]),
                        html.Td([
                            stock.info['dividendRate']
                        ]),                    
                        html.Td([
                            stock.info['52WeekChange']
                        ])
                    ]),
                ], className='styled-table')
            ]
        ),

        html.Div([
            #html.P([(stock.news)])
        ])
    ]
)

#Search Bar Functionality
@callback(
    Output(component_id='stock-chart', component_property='children'),
    Output(component_id='opCashFlow', component_property='children'),
    Output(component_id='pe', component_property='children'),
    Input('search', 'n_clicks'),
    State('input-1-state', 'value')
)
def search_ticker(n_clicks,ticker):
    print(ticker)
    stock = YF.Ticker(str(ticker))
    return stock, stock.info['operatingCashflow'], round(stock.info['trailingPE'],2)



if __name__ == "__main__":
    app.run_server(debug=True)
