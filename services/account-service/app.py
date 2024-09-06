from flask import Flask, jsonify, request

app = Flask(__name__)

accounts = []

@app.route('/accounts', methods=['GET'])
def get_accounts():
    return jsonify(accounts), 200

@app.route('/accounts', methods=['POST'])
def create_account():
    account = request.json
    accounts.append(account)
    return jsonify(account), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003,debug=True)
