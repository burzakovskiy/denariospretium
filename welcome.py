
import os
import socketio
import eventlet
import eventlet.wsgi
from flask import Flask, jsonify, render_template
from regression import Regression
import threading

pairs = ['BTC_DASH', 'BTC_ETH','BTC_XMR']
predictions={'BTC_DASH':{},'BTC_ETH':{}, 'BTC_XMR':{}}
sio = socketio.Server()
app = Flask(__name__)

regressions = [Regression(pair) for pair in pairs]
for regression in regressions:
	regression.init_model() 

def run():
	for regression in regressions:
		regression.predict()
		predictions[regression.pair]= regression.result
	sio.emit('data', predictions)
	threading.Timer(int(regressions[0].period), run).start()
run()	

@app.route('/')
def Welcome():
    return render_template('index.html')

    
@sio.on('get_data')
def send_data(sid, data):
	sio.emit('data', predictions)
	print('received ',data)
	
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app = socketio.Middleware(sio, app)
	eventlet.wsgi.server(eventlet.listen(('', int(port))), app)
	

