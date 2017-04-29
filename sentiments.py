import requests
import json
import twitter
import datetime


class Sentiments:
	def __init__(self):
		self.url = 'http://api.datumbox.com/1.0/TwitterSentimentAnalysis.json'
		self.sa_api_key ="5528495ca2e28e32621d7156035f2b2b"

		self.api = twitter.Api(consumer_key='RtktIiM25qJOzvImtINDxdxPR',
                      consumer_secret='26DQ7Dc2hGdbNDWx78J0r4vZJYFpfBx19AZraM5702xd5HbkWW',
                      access_token_key='819411021836222464-zvrUOci02zkVdlbXqx0O5bdMSOxZ4sm',
                      access_token_secret='vcu24xG83Ay794cVYIna146418UXqKKCtXdfgxEnBzvnc')
	
	def init(self):
		self.api.VerifyCredentials()
		print('Twitter connection has been established')
	
	def get_sentiments_ratio(self, pair):
		quote, base = pair.split('_')
		yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
		twitter_results = self.api.GetSearch(raw_query='q=%23'+base+'%20since%3A'+yesterday, result_type="popular")
		total = len(twitter_results)
		counter = {'negative':0, 'neutral':0, 'positive':0}
		
		for i in range(0,len(twitter_results)):
			r = requests.post(self.url, data = {'api_key':self.sa_api_key, 'text':twitter_results[i].text})
			data = json.loads(r.content)
			if 'result' in data['output']:
		   		counter[data['output']['result']]+=1
			else:
				total-=1
				print(data['output']['error'])
		print(counter)
		if(total != 0):
			counter['positive']=round((counter['positive']/total)*100,1)
			counter['negative']=round((counter['negative']/total)*100,1)
			counter['neutral']=round((counter['neutral']/total)*100,1)
		return counter
		