# stocks_scraped

A live KOSPI Stock viewer from scraping and cleaning real time stock data. Includes a chart, company's financial information, and daily stock information for specific tickers from a dropdown menu. Uses scikit-learn ML to predict stock prices for chosen stock.
Multiple algorithms are used and the algorithm with the highest score is chosen and used to predict the future prices. But the scores are not generally high (~0.7), and the prediction itself does not incorporate enough factors to give a reliable enough prediction
to invest one's money. Future improvements could involve additional metrics and incorporate more data from a wider point of view to produce a more reliable prediction.
