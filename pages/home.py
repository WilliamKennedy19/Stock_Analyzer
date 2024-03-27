import yfinance as YF
import dash
from dash import Dash,dcc,html, callback, clientside_callback,Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import json

dash.register_page(__name__,path="/")

stock = YF.Ticker("META")
stock_hist = YF.Ticker("META").history().reset_index()
stock_income = stock.income_stmt.set_axis(['2023', '2022', '2021','2020'], axis=1).reset_index()
stock_balance = stock.balance_sheet.set_axis(['2023', '2022', '2021','2020'], axis=1).reset_index()
stock_cashFlow = stock.cash_flow.set_axis(['2023', '2022', '2021','2020'], axis=1).reset_index()

data = (

    stock_hist.assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d")).sort_values(by="Date")

)

layout = html.Div([

    html.Div([
        html.H1(children="Stock Analyzer Tool"),

        html.H2(children=("Stock Information- {}".format(stock.info["longName"])),id="stock-main-title",className='chart-header'),
    ],id="chart-heading"),
    
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
                        stock.info.get("enterpriseValue")
                    ],id="enterprise"),
                    html.Td([
                        str(round(stock.info.get("grossMargins") * 100, 2)) + "%"
                    ],id="grossmargins"),
                    html.Td([
                        round(stock.info.get("trailingEps"), 2)
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
            ],className="styled-table"),
        ]
    ),

    html.H1("Statements for {}".format(str(stock.info['shortName'])) ),

    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
        dcc.Tab(label='Income Statement',children=[
            html.Div([
                dash_table.DataTable(data=stock_income.to_dict("records"))
            ],id="incomeStatement")
        ]),
        dcc.Tab(label='Balance Sheet', children=[
            html.Div([
                dash_table.DataTable(data=stock_balance.to_dict("records"))
            ],id="balanceSheet")
        ]),
        dcc.Tab(label="Cash Flow Statement",children=[
                    html.Div([
                        dash_table.DataTable(data=stock_cashFlow.to_dict("records"))
                    ],id="cashFlowStatement")
        ])
    ])   
],id="main-content")