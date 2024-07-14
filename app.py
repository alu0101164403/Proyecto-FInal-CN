from flask import Flask, render_template
from flask_socketio import SocketIO
import os
import csv
import time

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def read_csv_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def emit_data():
    while True:
        if os.path.exists('hdfs://10.6.129.98:9000/user/username/top_selling_products/part-00000'):
            top_selling_products = read_csv_file('hdfs://10.6.129.98:9000/user/username/top_selling_products/part-00000')
            socketio.emit('top_selling_products', top_selling_products)

        if os.path.exists('hdfs://10.6.129.98:9000/user/username/low_stock_products/part-00000'):
            low_stock_products = read_csv_file('hdfs://10.6.129.98:9000/user/username/low_stock_products/part-00000')
            socketio.emit('low_stock_products', low_stock_products)
        
        time.sleep(10)

@socketio.on('connect')
def handle_connect():
    emit_data()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)


