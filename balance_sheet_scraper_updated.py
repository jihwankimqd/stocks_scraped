import requests
import pandas as pd

def get_balance_sheet_updated(stockid):
    URL = "https://finance.naver.com/item/main.nhn?code="+str(stockid)

    samsung_electronic = requests.get(URL)

    financial_stmt = pd.read_html(samsung_electronic.text)[3]

    # financial_stmt.set_index(('주요재무정보', '주요재무정보', '주요재무정보'), inplace=True)
    # financial_stmt.set_index(('주요재무정보'), inplace=True)

    financial_stmt.index.rename('주요재무정보', inplace=True)
    financial_stmt.columns = financial_stmt.columns.droplevel(2)
    financial_stmt.columns = financial_stmt.columns.droplevel(0)

    df = pd.DataFrame(financial_stmt)
    # balance_sheet.reset_index(level=0,inplace=True)
    # cols = list(df.columns.values)
    # cols = ['주요재무정보','2017.12','2018.12','2019.03','2019.06','2019.09','2019.12','2020.03','2020.06(E)','2020.12(E)']
    cols = ['주요재무정보','2017.12','2018.12','2019.06','2019.09','2019.12','2020.03','2020.06','2020.09(E)']
    df = df[cols]
    # df.drop(['2017.12','2018.12','2020.12(E)'],axis = 1,inplace=True)
    df.drop(['2017.12','2018.12'],axis = 1,inplace=True)

    df.rename(columns={'주요재무정보':'Indicators'},inplace=True)
    df = df.set_index('Indicators')
    # df.columns = ['2019.03','2019.06','2019.09','2019.12(A)','2019.12','2020.03','2020.06(E)']
    df.columns = ['2019.06','2019.09','2019.12(A)','2019.12','2020.03','2020.06','2020.09(E)']

    # df = df[['2019.12(A)','2019.03','2019.06','2019.09','2019.12','2020.03','2020.06(E)']]
    df = df[['2019.06','2019.09','2019.12(A)','2019.12','2020.03','2020.06','2020.09(E)']]

    

    df.drop(df.index[[13,14,15]],inplace=True)
    df.drop('2019.12(A)',axis = 1,inplace=True)
    col = df.columns.values
    df[col] = df[col].astype(float)
    df = df.round(2)
    df.reset_index(inplace=True)
    df['Indicators'] = df['Indicators'].replace({'매출액': 'Sales(100mil Won)', '영업이익': 'Operating Revenue(100mil Won)', '당기순이익': 'Net Income(100mil Won)', '영업이익률': 'Operating Revenue(%)','순이익률': 'Net Income(%)', 'ROE(지배주주)': 'ROE', '부채비율': 'Liabilities(%)', '당좌비율': 'Quick Assets(%)', '유보율': 'Reserve Ratio(%)', 'EPS(원)': 'EPS(Won)', 'PER(배)': 'PER', 'BPS(원)': 'BPS(Won)', 'PBR(배)': 'PBR'})
    return df