import json
import requests
from kafka import KafkaProducer
import time

def fetch_sales_data():
    url = "http://localhost:5000/sales"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from API. Status code: {response.status_code}")
        return []

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    data = fetch_sales_data()
    if data:
        for sale in data:
            producer.send('supermarket-sales', sale)
            print(f"Sending sale: {sale} to Kafka")
    else:
        print("No data fetched from API. Retrying...")
    time.sleep(2)  # Espera 10 segundos antes de obtener nuevos datos
