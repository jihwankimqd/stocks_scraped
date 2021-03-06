# import os
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output
# import pandas as pd
# import pandas_datareader.data as web
# from datetime import datetime as dt
# from balance_sheet_scraper import get_balance_sheet

# # ###
# # url = 'https://raw.githubusercontent.com/jihwankimqd/stocks_scraped/master/kospi_data.csv'
# # df = pd.read_csv(url,sep=",")
# # col = ['기업명', '종목코드']
# # df1 = df[col].copy()
# # df1.columns = ['label','value']
# # df1['value'] = df1['value'].apply(str)
# # df1['value'] = df1['value'].str.zfill(6)
# # df1['label'] = df1['label']+' ('+df1['value']+')'
# # stock_data = df1.to_dict('records')
# # ###


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# server = app.server


# app.layout = html.Div([
#     html.Div([

#     html.H1('Live KOSPI Stock Viewer'),

#     ],style={'width': '100%', 'float': 'left', 'display': 'inline-block'}),

#     html.Div([
        
#         html.H2('Choose a Stock Ticker'),
#         dcc.Dropdown(
#             id='my-dropdown',
#             options=[
#             {'label': 'Samsung', 'value': '005930'},
#             {'label': 'SKInnovation', 'value': '096770'}
#         ],
#             # options=stock_data,
#             value='005930'
#         ),
    
#     ]),
#     html.Div([

#         html.H2('Stock Graph'),
#         dcc.Graph(id='my-graph'),
#         html.P('')
    
#     ],style={'width': '100%', 'float': 'left', 'display': 'inline-block'}),

#     html.Div([
#         html.H4(children='Stock Data'),
#         html.Table(id='stock-table'),
#         html.P('')


#     ],style={'width':'40%','float': 'right', 'display': 'inline-block'}),
#     html.Div([
#         html.H4(children='Financial Information'),
#         html.Table(id='balance-table'),
#         html.P('')

#     ],style={'width':'40%','float': 'left', 'display': 'inline-block'})

# ])

# # Stock Table
# @app.callback(Output('stock-table', 'children'), [Input('my-dropdown', 'value')])
# def generate_stock_table(stock_id, max_rows=17):
#     # Get stock data using web.DataReader(), which conveniently has a built-in function for Naver Finance
#     dataframe = web.DataReader(stock_id, 'naver', start='2015-01-01', end=dt.now()).reset_index()
#     dataframe['Date'] = pd.to_datetime(dataframe['Date']).dt.date
#     return html.Table([
#         html.Thead(
#             html.Tr([html.Th(col) for col in dataframe.columns])
#         ),
#         html.Tbody([
#             html.Tr([
#                 html.Td(dataframe.iloc[-i-1][col]) for col in dataframe.columns
#             ]) for i in range(min(len(dataframe), max_rows))
#         ])
#     ])

# # Balance Sheet
# # @app.callback(Output('balance-table', 'children'), [Input('my-dropdown', 'value')])
# # def generate_balance_table(stock_id, max_rows=16):
# #     dataframe = get_balance_sheet(stock_id)
# #     return html.Table([
# #         html.Thead(
# #             html.Tr([html.Th(col) for col in dataframe.columns])
# #         ),
# #         html.Tbody([
# #             html.Tr([
# #                 html.Td(dataframe.iloc[-i-1][col]) for col in dataframe.columns
# #             ]) for i in range(min(len(dataframe), max_rows))
# #         ])
# #     ])

# # Stock Graph
# @app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
# def update_graph(stock_id):
#     dataframe = web.DataReader(stock_id, 'naver', start='2015-01-01', end=dt.now()).reset_index()
#     dataframe['Date'] = pd.to_datetime(dataframe['Date']).dt.date
#     return {
#         'data': [{
#             'x': dataframe.Date,
#             'y': dataframe.Close
#         }]
#     }

# if __name__ == '__main__':
#     app.run_server(debug=True)


import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import pandas_datareader.data as web

from datetime import datetime as dt

from balance_sheet_scraper import get_balance_sheet
from balance_sheet_scraper_updated import get_balance_sheet_updated


from stock_predictor import stock_predict

import plotly.tools as tls


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)


server = app.server

###
url = 'https://raw.githubusercontent.com/jihwankimqd/stocks_scraped/master/kospi_data.csv'
df = pd.read_csv(url,sep=",")
col = ['기업명', '종목코드']
df1 = df[col].copy()
df1.columns = ['label','value']
df1['value'] = df1['value'].apply(str)
df1['value'] = df1['value'].str.zfill(6)
df1['label'] = df1['label']+' ('+df1['value']+')'
stock_data = df1.to_dict('records')
###

app.layout = html.Div([

    dcc.Link(
    html.Button('Github'),
    href='https://github.com/jihwankimqd/stocks_scraped', target="_blank"),

    html.H2('Choose Your Stock'),

    html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        options=stock_data,
        value='005930'
    ),
    ],style={'width': '24%', 'float': 'left', 'display': 'inline-block'}),

    html.Div([
    html.Br(),
    html.Br()

    ]),

    # html.Div([
    # html.H2('Stock Graph'),
    # dcc.Graph(id='my-graph'),
    # html.P(''),
    # ],style={'width': '100%', 'display': 'inline-block'}),

    html.Div([
    # html.H2('Predicted Price Graph Using ML'),
    dcc.Graph(id='stock_prediction'),
    html.P(''),
    ],style={'width':'100%','display': 'inline-block'}),


    html.Div([
    html.H4(children='Stock Data'),
    html.Table(id='stock-table'),
    html.P(''),
    ],style={'width': '40%', 'float': 'right', 'display': 'inline-block'}),

    html.Div([
    html.H4(children='Financial Information'),
    html.Table(id='balance-table'),
    html.P('')
    ],style={'width': '55%', 'float': 'left', 'display': 'inline-block'}),




    html.Div(id='display-value'),

    
])

# Stock Table
@app.callback(Output('stock-table', 'children'), [Input('my-dropdown', 'value')])
def generate_stock_table(stock_id, max_rows=17):
    # Get stock data using web.DataReader(), which conveniently has a built-in function for Naver Finance
    dataframe = web.DataReader(stock_id, 'naver', start='2015-01-01', end=dt.now()).reset_index()
    dataframe['Date'] = pd.to_datetime(dataframe['Date']).dt.date
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[-i-1][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

# Balance Sheet
@app.callback(Output('balance-table', 'children'), [Input('my-dropdown', 'value')])
def generate_balance_table(stock_id, max_rows=16):
    # Samsung released new figures, but other companies are slower at updating their figures.
    
    try:
        dataframe = get_balance_sheet_updated(stock_id)
    except KeyError:
        dataframe = get_balance_sheet(stock_id)

    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[-i-1][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

# # Stock Graph
# @app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
# def update_graph(stock_id):
#     dataframe = web.DataReader(stock_id, 'naver', start='2015-01-01', end=dt.now()).reset_index()
#     dataframe['Date'] = pd.to_datetime(dataframe['Date']).dt.date
#     return {
#         'data': [{
#             'x': dataframe.Date,
#             'y': dataframe.Close
#         }]
#     }

# Stock Prediction
@app.callback(Output('stock_prediction', 'figure'), [Input('my-dropdown', 'value')])
def update_prediction(stock_id):
    dataframe = stock_predict(stock_id)
    # predicted = dataframe.Close + dataframe.Forecast

    fig = tls.make_subplots(rows=1, cols=1, shared_xaxes=True,vertical_spacing=0.009,horizontal_spacing=0.009)
    fig['layout']['margin'] = {'l': 50, 'r': 0, 'b': 50, 't': 50}

    # fig.append_trace({'x':dataframe.index,'y':dataframe.Close,'type':'scatter','name':'Historical Price'},1,1)
    # fig.append_trace({'x':dataframe.index,'y':dataframe.Forecast,'type':'scatter','name':'Predicted Price'},1,1)
    fig.append_trace({'x':dataframe.index,'y':dataframe.Close,'type':'scatter','name':'Historical Price'},1,1)
    fig.append_trace({'x':dataframe.index,'y':dataframe.Forecast,'type':'scatter','name':'Predicted Price'},1,1)
    return fig

            
if __name__ == '__main__':
    app.run_server(debug=True)