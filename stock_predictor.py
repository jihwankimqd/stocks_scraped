import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import numpy as np
from sklearn import preprocessing

import pandas_datareader.data as web
from datetime import datetime as dt
import datetime

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR

def stock_predict(stockid):
    df = web.DataReader(str(stockid), 'naver', start='2015-01-01', end=dt.now()).reset_index()
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df.set_index('Date',inplace=True)
    df.sort_values(by=['Date'],inplace=True,ascending = True)
    df[['Open','High','Low','Close','Volume']] = df[['Open','High','Low','Close','Volume']].astype(int)
    dfreg = df.loc[:,['Close' , 'Volume']]
    dfreg['HL_PCT'] = (df['High']-df['Low']) / df['Close'] *100.0
    dfreg['PCT_change'] = (df['Close']-df['Open']) / df['Open'] *100.0

    dfreg.head()

    # Check for null values and should drop them if existing
    # dfreg.isnull().sum()


    # We want to separate 1 percent of the data to forecast
    forecast_out = int(math.ceil(0.03 * len(dfreg)))
    # Separating the label here, we want to predict the AdjClose
    forecast_col = 'Close'
    dfreg['label'] = dfreg[forecast_col].shift(-forecast_out)

    dfreg.dropna()

    X = np.array(dfreg.drop(['label'], 1))

    # Set infinity to 0
    X[X >= 1E308] = 0
    dfreg.head()

    # Scale the X so that everyone can have the same distribution for linear regression
    X = preprocessing.scale(X)

    # Finally We want to find Data Series of late X and early X (train) for model generation and evaluation
    X_lately = X[-forecast_out:]
    X = X[:-forecast_out]

    # Separate label and identify it as y
    y = np.array(dfreg['label'])
    y = y[:-forecast_out]





    X_train,X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Linear regression
    clfreg = LinearRegression(n_jobs=-1)
    clfreg.fit(X_train, y_train)

    # Quadratic Regression 2
    clfpoly2 = make_pipeline(PolynomialFeatures(2), Ridge())
    clfpoly2.fit(X_train, y_train)

    # Quadratic Regression 3
    clfpoly3 = make_pipeline(PolynomialFeatures(3), Ridge())
    clfpoly3.fit(X_train, y_train)

    # KNN Regression
    clfknn = KNeighborsRegressor(n_neighbors=2)
    clfknn.fit(X_train, y_train)

    #SVM SVR
    clfsvm = SVR(kernel='rbf', C=1e3, gamma=0.1) 
    clfsvm.fit(X_train, y_train)

    confidencereg = clfreg.score(X_test, y_test)
    confidencepoly2 = clfpoly2.score(X_test,y_test)
    confidencepoly3 = clfpoly3.score(X_test,y_test)
    confidenceknn = clfknn.score(X_test, y_test)
    confidencesvm = clfsvm.score(X_test,y_test)

    algorithm_scores = {clfreg:confidencereg,
                        clfpoly2:confidencepoly2,
                        clfpoly3:confidencepoly3,
                        clfknn:confidenceknn,
                        clfsvm:confidencesvm}

    best_score = max(algorithm_scores, key = algorithm_scores.get)

    print(best_score)



    # recast_set = clfreg.predict(X_lately)
    # # forecast_set = clfpoly3.predict(X_lately)
    forecast_set = best_score.predict(X_lately)

    dfreg['Forecast'] = np.nan

    # length of forecast_set is equivalent to count of forecast_out
    # print(forecast_set)

    # print(confidencereg)
    # print(confidencepoly2)
    # print(confidencepoly3)
    # print(confidenceknn)
    # print(confidencesvm)

    last_date = dfreg.index[-1]
    # print(last_date)
    last_unix = last_date
    next_unix = last_unix + datetime.timedelta(days=1)

    for i in forecast_set:
        next_date = next_unix
        next_unix += datetime.timedelta(days=1)
        dfreg.loc[next_date, 'Forecast'] = i

    # dfreg = dfreg.dropna(subset=['Close'],axis=0)
    # dfreg = dfreg.dropna(subset=['Forecast'],axis=0)

    # dfreg['Predicted'] = pd.concat([dfreg['Close'], dfreg['Forecast']], axis=0)

    # dfreg['Close'] = dfreg['Close'].dropna()
    # dfreg['Forecast'] = dfreg['Forecast'].dropna()


    # print(dfreg['Close'])
    # print(dfreg['Forecast'])
    # print(dfreg['Predicted'])

    # dfreg['Close'].plot()
    # dfreg['Forecast'].plot()
    # plt.legend(loc=4)
    # plt.xlabel('Date')
    # plt.ylabel('Price')
    # plt.show()

    return dfreg

dataframe = stock_predict('005930')
# print(dataframe.Predicted)
