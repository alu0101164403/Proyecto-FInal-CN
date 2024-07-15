from flask import Flask, render_template
from flask_socketio import SocketIO
import os
import csv
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Permitir conexiones desde todos los orígenes

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
    try:
        while True:
            top_selling_products = []
            if os.path.exists('hdfs:///10.6.129.98:9000/user/username/top_selling_products/part-00000-4c9d81de-016c-4db3-bea1-523c2210c608-c000.csv'):
                top_selling_products = read_csv_file('hdfs:///10.6.129.98:9000/user/username/top_selling_products/part-00000-4c9d81de-016c-4db3-bea1-523c2210c608-c000.csv')

            socketio.emit('top_selling_products', top_selling_products)

            time.sleep(10)
    except Exception as e:
        print(f"Error en emit_data: {str(e)}")

@socketio.on('connect')
def handle_connect():
    emit_data()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
