import pandas as pd
from sklearn import cross_validation
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import time
import datetime
import requests
import json

class Regression:
	def __init__(self, pair):
		self.pair = pair
		self.period = '7200'
		self.clf = LinearRegression()
		self.result={}
		
	def init_model(self):
		train_df = pd.read_csv('./model/'+self.pair+'_proc.csv', index_col=0)
		X = train_df[['open', 'close','high','low','btc_close','volume']]
		y= train_df['label']
		X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size = 0.25)
		del train_df
		self.clf.fit(X_train,y_train)
		confidence = self.clf.score(X_test,y_test)
		print('Confidence '+str(confidence))
		se = mean_squared_error(y_test, self.clf.predict(X_test))
		print('Squared error '+str(se))
		
	
	def predict(self):
		def getStartTime():
		    currentTime = int(time.time())
		    timeFrameEnd = int(self.period) - currentTime % int(self.period) + currentTime;
		    return str(timeFrameEnd - 13*int(self.period));
		
		url = ' https://poloniex.com/public?command=returnChartData&currencyPair='+self.pair+'&start='+getStartTime()+'&end=9999999999&period='+self.period
		r = requests.get(url)
  		data = json.loads(r.content)
   		df = pd.DataFrame(data)
   		df = df.set_index('date')
   		url = ' https://poloniex.com/public?command=returnChartData&currencyPair=USDT_BTC&start='+getStartTime()+'&end=9999999999&period='+self.period
   		r = requests.get(url)
   		data = json.loads(r.content)
   		df_btc = pd.DataFrame(data)
   		df_btc = df_btc.set_index('date')
   		df['btc_close'] = df_btc['close']
   		X = df[['open', 'close','high','low','btc_close','volume']]
   		predictions = self.clf.predict(X)
		df_result = df.copy()
		df_result['time_prediction'] = df_result.index.values +13*int(self.period)
		df_result['prediction'] =predictions
		df_result.set_index('time_prediction', inplace=True)
		self.result = df_result['prediction'].to_dict()
		
		
		
	

		
		
	
		