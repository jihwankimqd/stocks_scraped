import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime as dt
import requests


###
# url = 'https://raw.githubusercontent.com/jihwankimqd/stocks_scraped/master/kospi_data.csv'
# df = pd.read_csv(url,sep=",")
df = pd.read_csv('kospi_data.csv')
col = ['기업명', '종목코드']
df1 = df[col].copy()
df1.columns = ['label','value']
df1['value'] = df1['value'].apply(str)
df1['value'] = df1['value'].str.zfill(6)
df1['label'] = df1['label']+' ('+df1['value']+')'
stock_data = df1.to_dict('records')
###

def get_balance_sheet(stockid):
    URL = "https://finance.naver.com/item/main.nhn?code="+str(stockid)

    samsung_electronic = requests.get(URL)
    html = samsung_electronic.text

    financial_stmt = pd.read_html(samsung_electronic.text)[3]

    # financial_stmt.set_index(('주요재무정보', '주요재무정보', '주요재무정보'), inplace=True)
    # financial_stmt.set_index(('주요재무정보'), inplace=True)

    financial_stmt.index.rename('주요재무정보', inplace=True)
    financial_stmt.columns = financial_stmt.columns.droplevel(2)
    financial_stmt.columns = financial_stmt.columns.droplevel(0)

    df = pd.DataFrame(financial_stmt)
    # balance_sheet.reset_index(level=0,inplace=True)
    # cols = list(df.columns.values)
    cols = ['주요재무정보','2017.12','2018.12','2019.03','2019.06','2019.09','2019.12','2020.03','2020.06(E)','2020.12(E)']
    df = df[cols]
    df.drop(['2017.12','2018.12','2020.12(E)'],axis = 1,inplace=True)
    df.rename(columns={'주요재무정보':'Indicators'},inplace=True)
    df = df.set_index('Indicators')
    df.columns = ['2019.03','2019.06','2019.09','2019.12(A)','2019.12','2020.03','2020.06(E)']
    df = df[['2019.12(A)','2019.03','2019.06','2019.09','2019.12','2020.03','2020.06(E)']]
    df.drop(df.index[[13,14,15]],inplace=True)
    df.drop('2019.12(A)',axis = 1,inplace=True)
    col = df.columns.values
    df[col] = df[col].astype(float)
    df = df.round(2)
    df.reset_index(inplace=True)
    df['Indicators'] = df['Indicators'].replace({'매출액': 'Sales(100mil Won)', '영업이익': 'Operating Revenue(100mil Won)', '당기순이익': 'Net Income(100mil Won)', '영업이익률': 'Operating Revenue(%)','순이익률': 'Net Income(%)', 'ROE(지배주주)': 'ROE', '부채비율': 'Liabilities(%)', '당좌비율': 'Quick Assets(%)', '유보율': 'Reserve Ratio(%)', 'EPS(원)': 'EPS(Won)', 'PER(배)': 'PER', 'BPS(원)': 'BPS(Won)', 'PBR(배)': 'PBR'})
    return df

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


app.layout = html.Div([
    html.Div([

    html.H1('Live KOSPI Stock Viewer'),

    ],style={'width': '100%', 'float': 'left', 'display': 'inline-block'}),

    html.Div([
        
        html.H2('Choose a Stock Ticker'),
        dcc.Dropdown(
            id='my-dropdown',
        #     options=[
        #     {'label': 'Samsung', 'value': '005930'},
        #     {'label': 'SKInnovation', 'value': '096770'}
        # ],
            options=stock_data,
            value='005930'
        ),
    
    ]),
    html.Div([

        html.H2('Stock Graph'),
        dcc.Graph(id='my-graph'),
        html.P('')
    
    ],style={'width': '100%', 'float': 'left', 'display': 'inline-block'}),

    html.Div([
        html.H4(children='Stock Data'),
        html.Table(id='stock-table'),
        html.P('')


    ],style={'width':'40%','float': 'right', 'display': 'inline-block'}),
    html.Div([
        html.H4(children='Financial Information'),
        html.Table(id='balance-table'),
        html.P('')

    ],style={'width':'40%','float': 'left', 'display': 'inline-block'})

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

# Stock Graph
@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(stock_id):
    dataframe = web.DataReader(stock_id, 'naver', start='2015-01-01', end=dt.now()).reset_index()
    dataframe['Date'] = pd.to_datetime(dataframe['Date']).dt.date
    return {
        'data': [{
            'x': dataframe.Date,
            'y': dataframe.Close
        }]
    }

if __name__ == '__main__':
    app.run_server(debug=True)


