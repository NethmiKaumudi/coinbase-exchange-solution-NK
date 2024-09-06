import random

from flask import Flask, jsonify

app = Flask(__name__)

# Dummy crypto price data
crypto_prices = {"BTC": round(random.uniform(20000, 50000), 2), "ETH": round(random.uniform(1500, 3500), 2),
                 "LTC": round(random.uniform(100, 300), 2), }


@app.route('/crypto-prices', methods=['GET'])
def get_crypto_prices():
    return jsonify(crypto_prices), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
