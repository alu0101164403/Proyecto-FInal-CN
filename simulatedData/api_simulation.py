from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

products = ["Apple", "Banana", "Carrot", "Doughnut", "Egg", "Fish", "Grapes", "Honey", "Ice Cream", "Juice"]
prices = [1.0, 0.5, 0.8, 1.5, 0.2, 2.0, 1.2, 3.0, 2.5, 1.5]

@app.route('/sales', methods=['GET'])
def get_sales_data():
    sales_data = []
    for _ in range(random.randint(5, 15)):
        product = random.choice(products)
        quantity = random.randint(1, 5)
        price = prices[products.index(product)]
        sales_data.append({
            "product": product,
            "quantity": quantity,
            "price": price,
            "timestamp": time.time()
        })
    return jsonify(sales_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
