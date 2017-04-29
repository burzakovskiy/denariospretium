
import os
import socketio
import eventlet
import eventlet.wsgi
from flask import Flask, jsonify, render_template
from regression import Regression
import threading
from sentiments import Sentiments

pairs = ['BTC_DASH', 'BTC_ETH','BTC_XMR','BTC_LTC','BTC_XRP']
output_data={'BTC_DASH':{
				'predictions':{},
				'sentiments':{}
			},'BTC_ETH':{
				'predictions':{},
				'sentiments':{}
			}, 'BTC_XMR':{
				'predictions':{},
				'sentiments':{}
			},'BTC_LTC':{
				'predictions':{},
				'sentiments':{}
			},'BTC_XRP':{
				'predictions':{},
				'sentiments':{}
			}}
sio = socketio.Server()
app = Flask(__name__)

sentiments = Sentiments()
sentiments.init()

regressions = [Regression(pair) for pair in pairs]
for regression in regressions:
	regression.init_model() 

def run():
	print('Running data analysis')
	for regression in regressions:
		regression.predict()
		output_data[regression.pair]['predictions']= regression.result
		output_data[regression.pair]['sentiments']=sentiments.get_sentiments_ratio(regression.pair)
	sio.emit('data', output_data)
	
	threading.Timer(int(regressions[0].period), run).start()
	
threading.Thread(target=run, args=()).start()

@app.route('/')
def Welcome():
    return render_template('index.html')

    
@sio.on('get_data')
def send_data(sid, data):
	sio.emit('data', output_data)
	print('received ',data)
	
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app = socketio.Middleware(sio, app)
	eventlet.wsgi.server(eventlet.listen(('', int(port))), app)
	


