from flask import Flask, jsonify, request

app = Flask(__name__)

transactions = []

@app.route('/transactions', methods=['GET'])
def get_transactions():
    return jsonify(transactions), 200

@app.route('/transactions', methods=['POST'])
def create_transaction():
    transaction = request.json
    transactions.append(transaction)
    return jsonify(transaction), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
