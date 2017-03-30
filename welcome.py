
import os
import socketio
import eventlet
import eventlet.wsgi
from flask import Flask, jsonify, render_template
from regression import Regression
import threading

pair = 'BTC_DASH'
sio = socketio.Server()
app = Flask(__name__)

regression = Regression(pair)
regression.init_model()

def run():
	regression.predict()
	sio.emit('data', regression.result)
	threading.Timer(int(regression.period), run).start()
run()	

@app.route('/')
def Welcome():
    return render_template('index.html')

#@sio.on('connect')
#def connect(sid, environ):
#	print("connect ", sid)
#    
#@sio.on('disconnect')
#def disconnect(sid):
#    print('disconnect ', sid)
    
@sio.on('get_data')
def send_data(sid, data):
	sio.emit('data', regression.result)
	print('received ',data)
	
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app = socketio.Middleware(sio, app)
	eventlet.wsgi.server(eventlet.listen(('', int(port))), app)
#	app.run(host='0.0.0.0', port=int(port))
	

