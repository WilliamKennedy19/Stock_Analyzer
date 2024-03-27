import yfinance as YF
import dash
from dash import Dash,dcc,html, callback, clientside_callback,Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import json


stock = YF.Ticker("META")
stock_hist = YF.Ticker("META").history().reset_index()


stock_income = stock.income_stmt.set_axis(['2023', '2022', '2021','2020'], axis=1).reset_index()
stock_balance = stock.balance_sheet.set_axis(['2023', '2022', '2021','2020'], axis=1).reset_index()
stock_cashFlow = stock.cash_flow.set_axis(['2023', '2022', '2021','2020'], axis=1).reset_index()

data = (

    stock_hist.assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d")).sort_values(by="Date")

)

app = Dash(__name__,external_stylesheets=['assets/style.css'],use_pages=True)

#
# Main app layout for the Stock Information Screen
app.layout = html.Div(

    children=[
        html.Div([
            html.Ul([
                html.Li([
                    html.Button("Home",className="dropbtn"),
                    html.Div([
                        html.A("Home",href="/"),
                        html.A("Statements"),
                        html.A("Fundamental Analysis"),
                        html.A("Technical Analysis")
                    ],className="dropdown-content")
                ],className="dropdown"),
                html.Li([
                    html.Div([
                        html.Button([html.I(className="fas fa-search")], id="search",className='btn-search', n_clicks=0),
                        dcc.Input(id="input-1-state",className='input-search', type='text', placeholder='Enter search query...')
                    ],className="search-box"),
                ])
            ],className="navbar")
        ],id="navbar-container"), 
        
        dash.page_container
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
    Output(component_id='freeCashFlow', component_property='children'),
    Output(component_id='returnOnAssets', component_property='children'),
    Output(component_id='totalDebt', component_property='children'),
    Output(component_id='ebitda', component_property='children'),
    Output(component_id='sharesOutstanding', component_property='children'),
    Output(component_id='dividendYield', component_property='children'),
    Output(component_id='dividendRate', component_property='children'),
    Output(component_id='52WeekChange', component_property='children'),
    Output(component_id="stock-main-title",component_property='children'),
    #Output(component_id="statementsTitle", component_property="children"),
    Output(component_id="incomeStatement",component_property="children"),
    Output(component_id="balanceSheet",component_property="children"),
    Output(component_id="cashFlowStatement",component_property="children"),
    Input('search', 'n_clicks'),
    State('input-1-state', 'value')
)
def search_ticker(n_clicks,ticker):
    stock = YF.Ticker(str(ticker))
    stock_hist = stock.history().reset_index()

    data = (stock_hist.assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d")).sort_values(by="Date"))

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
                #statementsTitle,
                income,
                balance,
                cashFlow
            )




if __name__ == "__main__":
    app.run_server(debug=True)
