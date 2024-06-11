import eventlet
eventlet.monkey_patch()
import json
from flask import Flask, render_template, request
from flask_mqtt import Mqtt
from flask_socketio import SocketIO, emit
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_CLEAN_SESSION'] = True
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)

client_topics = {}  # Tiene traccia dei topic a cui ogni client è interessato
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    sid = request.sid
    print(f'Client connected: {sid}')
    emit('client_connected', sid)  # Emit un evento 'client_connected' con l'identificatore del client
    available_topics = ['ping', 'bandwidth', 'iperf', 'http_response_time']
    socketio.emit('available_topics', available_topics) # Emit dei topic disponibili
    client_topics[sid] = set()  # Inizializza i topic del client come un insieme vuoto

@socketio.on('publish')
def handle_publish(data):
    topic = data['topic']           # Estrazione dati
    message = data['message']
    mqtt.publish(topic, message)    # Pubblicazione del messaggio sul topic specifico
    print("Messaggio pubblicato correttamente") 

@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data['topic'])
    client_topics[request.sid].add(data['topic'])  # Aggiungi il topic al set dei topic del client
    
@socketio.on('unsubscribe')
def handle_unsubscribe(json_str):
    data = json.loads(json_str)
    mqtt.unsubscribe(data['topic'])
    client_topics[request.sid].remove(data['topic'])  # Rimuovi il topic dal set dei topic del client

@mqtt.on_message() 
def handle_mqtt_message(client, userdata,message):
    for client_id, topics in client_topics.items():
        if message.topic in topics:
            data = dict(
                topic=message.topic,
                payload=message.payload.decode(),
            )
            socketio.emit('mqtt_message', data=data, room=client_id)  # Instrada il messaggio solo ai client interessati

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)
