import socketio
import time
import subprocess
import re
import requests
import psutil
import json

sio = socketio.Client()

# Connessione al server Flask
sio.connect('http://localhost:5000') 

@sio.event
def connect():
    print('Connected to Flask server')

@sio.event
def disconnect():
    print('Disconnected from Flask server')

def get_ping():
    result = subprocess.run(["ping", "-c", "4", "www.google.it"], capture_output=True, text=True)
    output = result.stdout
    times = re.findall(r'time=(\d+\.\d+)', output) # Estrai i tempi di risposta
    times = [float(time) for time in times]# Converti i tempi estratti in numeri float
    # Calcola la media dei tempi
    if times:
        message = sum(times) / len(times)
    else:
        message = None
    return message

def get_bandwidth():
    counters = psutil.net_io_counters()
    bytes_transferred = counters.bytes_sent + counters.bytes_recv
    bandwidth_mb_rounded = round((bytes_transferred / (10 ** 6)), 2)  # Conversione e arrotondamento
    return bandwidth_mb_rounded

def get_iperf():
    output = subprocess.run(["iperf3", "-c", "iperf.he.net", "--json"], capture_output=True)
    if output.returncode == 0:
        result = json.loads(output.stdout)
        if 'end' in result and 'sum_received' in result['end'] and 'bits_per_second' in result['end']['sum_received']:
            bitrate = result['end']['sum_received']['bits_per_second'] / 1e6  #Conversione
            return f"{bitrate:.2f}"  # Arrotondamento
    return None

def get_http_response_time():
    url="https://www.google.com"
    response = requests.head(url)
    if response: 
        return round(response.elapsed.total_seconds() * 1000, 2)  # Conversione e arrotondamento
    return None
    
while True:
    # Genera dati casuali per i diversi topic
    ping_value = get_ping()
    bandwidth_value = get_bandwidth()
    iperf_value = get_iperf()
    http_response_time_value = get_http_response_time()
    
    if ping_value is not None:
        sio.emit('publish', {'topic': 'ping', 'message': ping_value})
    
    if bandwidth_value is not None:   
        sio.emit('publish', {'topic': 'bandwidth', 'message': bandwidth_value})
    
    if iperf_value is not None:
        sio.emit('publish', {'topic': 'iperf', 'message': iperf_value})
    
    if http_response_time_value is not None:
        sio.emit('publish', {'topic': 'http_response_time', 'message': http_response_time_value})#correggere perche non funziona
    
    time.sleep(5)  # Wait
