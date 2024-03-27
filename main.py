import yfinance as YF
from dash import Dash,dcc,html, callback, clientside_callback,Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import json

stock = YF.Ticker("META")
stock_hist = YF.Ticker("META").history().reset_index()

data = (

    stock_hist.query("Dividends==0.0").assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d")).sort_values(by="Date")

)

app = Dash(__name__,external_stylesheets=['assets/style.css'])

#
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

        
        html.Div([
            dcc.Graph(

                figure={

                    "data": [

                        {

                            "x": data["Date"],

                            "y": data["Close"],

                        },

                    ],

                    "layout": {"title": f"{stock.info['shortName']} (META) - Daily Price Changes"},

                },

            ),
        ],id="stockchart"),
        

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
                                
                        ],id="enterprise"),
                        html.Td([
                                
                        ],id="grossmargins"),
                        html.Td([
                                
                        ],id="eps"),
                        html.Td([
                                
                        ],id="market_cap"),
                        html.Td([
                                
                        ],id="revGrowth"),                    
                        html.Td([
                                
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
                        ],id="freeCashFlow"),
                        html.Td([
                            stock.info['returnOnAssets']
                        ],id="returnOnAssets"),
                        html.Td([
                            stock.info['totalDebt']
                        ],id="totalDebt"),
                        html.Td([
                            stock.info['ebitda']
                        ],id="ebitda"),
                        html.Td([
                            stock.info['sharesOutstanding']
                        ],id="sharesOutstanding"),
                        html.Td([
                            stock.info['dividendYield']
                        ],id="dividendYield"),
                        html.Td([
                            stock.info['dividendRate']
                        ],id="dividendRate"),                    
                        html.Td([
                            stock.info['52WeekChange']
                        ],id="52WeekChange")
                ], className='styled-table')
            ]
        ),

        html.H1("Statements for {}".format(str(stock.info['shortName'])) ),
    
        html.Div([
            html.H2("Income Statement"),
            dash_table.DataTable(data=stock_income.to_dict("records"))
        ],id="incomeStatement"),
    
        html.Div([
            html.H2("Balance Sheet"),
            dash_table.DataTable(data=stock_balance.to_dict("records"))
        ],id="balanceSheet"),
    
        html.Div([
            html.H2("Cash Flow Statement"),
            dash_table.DataTable(data=stock_cashFlow.to_dict("records"))
        ],id="cashFlowStatement")
    ]
)

#Search Bar Functionality
@callback(
    Output(component_id='stockchart', component_property='children'),
    Output(component_id='opCashFlow', component_property='children'),
    Output(component_id='pe', component_property='children'),
    Output(component_id='enterprise', component_property='children'),
    Output(component_id='grossmargins', component_property='children'),
    Output(component_id='eps', component_property='children'),
    Output(component_id='market_cap', component_property='children'),
    Output(component_id='revGrowth', component_property='children'),
    Output(component_id='52weekHigh', component_property='children'),
    Output(component_id='52weekHigh', component_property='children'),
    Output(component_id='freeCashFlow', component_property='children'),
    Output(component_id='returnOnAssets', component_property='children'),
    Output(component_id='totalDebt', component_property='children'),
    Output(component_id='ebitda', component_property='children'),
    Output(component_id='sharesOutstanding', component_property='children'),
    Output(component_id='dividendYield', component_property='children'),
    Output(component_id='dividendRate', component_property='children'),
    Output(component_id='52WeekChange', component_property='children'),
    Output(component_id="stock-info-title",component_property='children'),
    Output(component_id="statementsTitle", component_property="children"),
    Output(component_id="incomeStatement",component_property="children"),
    Output(component_id="balanceSheet",component_property="children"),
    Output(component_id="cashFlowStatement",component_property="children"),
    Input('search', 'n_clicks'),
    State('input-1-state', 'value')
)
def search_ticker(n_clicks,ticker):
    stock = YF.Ticker(str(ticker))
    stock_hist = stock.history().reset_index()

    data = (stock_hist.query("Dividends==0").assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d")).sort_values(by="Date"))

    stock_info = stock.info

    chart = html.Div([dcc.Graph(

            figure={

                "data": [

                    {

                        "x": data["Date"],

                        "y": data["Close"],

                    },

                ],

                "layout": {"title": f"{stock.info['shortName']} ({str.upper(ticker)}) - Daily Price Changes"},

            },

        )])
    try:
        opCashFlow = stock_info.get("operatingCashflow")
    except():
         opCashFlow = "NA"

    try: 
        pe = round(stock_info.get("trailingPE"), 2)
    except(TypeError):
        pe = "NA"

    enterprise = stock_info.get("enterpriseValue")
    grossmargins = str(round(stock_info.get("grossMargins") * 100, 2)) + "%"
    eps = round(stock_info.get("trailingEps"), 2)
    market_cap = stock_info.get("marketCap")
    revGrowth = stock_info.get("revenueGrowth")
    fiftyTwoWeekHigh = stock_info.get("fiftyTwoWeekHigh")
    freeCashFlow = stock_info.get('freeCashflow')
    returnAssets = stock_info.get('returnOnAssets')
    totalDebt = stock_info.get('totalDebt')
    ebitda = stock_info.get('ebitda')
    shares = stock_info.get('sharesOutstanding')
    dYield = stock_info.get('dividendYield')
    dRate = stock_info.get('dividendRate')
    fiftyTwoWeekChange = stock_info.get('52WeekChange')
    longName = "Stock Information- {}".format(stock.info["longName"])

    stock_income = stock.income_stmt.set_axis(['2023', '2022', '2021','2020'], axis=1).reset_index()
    stock_balance = stock.balance_sheet.set_axis(['2023', '2022', '2021','2020'], axis=1).reset_index()
    stock_cashFlow = stock.cash_flow.set_axis(['2023', '2022', '2021','2020'], axis=1).reset_index()
    
    statementsTitle = "Statements for {}".format(str(stock.info['shortName'])),

    income = html.Div([
        html.H2("Income Statement"),
        dash_table.DataTable(data=stock_income.to_dict("records"))
    ])

    balance = html.Div([
        html.H2("Balance Sheet"),
        dash_table.DataTable(data=stock_balance.to_dict("records"))
    ])

    cashFlow = html.Div([
        html.H2("Cash Flow Statement"),
        dash_table.DataTable(data=stock_cashFlow.to_dict("records"))
    ])


    return (    chart,
                opCashFlow,
                pe,
                enterprise,
                grossmargins,
                eps,
                market_cap,
                revGrowth,
                fiftyTwoWeekHigh,
                freeCashFlow,
                returnAssets,
                totalDebt,
                ebitda,
                shares,
                dYield,
                dRate,
                fiftyTwoWeekChange,
                longName,
                statementsTitle,
                income,
                balance,
                cashFlow
            )




if __name__ == "__main__":
    app.run_server(debug=True)
