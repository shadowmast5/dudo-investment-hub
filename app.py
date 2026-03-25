from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

users = {}
transactions = []
machines_owned = {}

@app.route('/')
def home():
    return "DUDO Backend Running"

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    users[data['phone']] = {"balance": 0, "referrals": 0}
    return jsonify({"message": "User registered"})

@app.route('/rent', methods=['POST'])
def rent():
    data = request.json
    phone = data['phone']
    amount = data['amount']
    machine_id = data['machine_id']

    transactions.append({
        "phone": phone,
        "amount": amount,
        "machine": machine_id,
        "date": str(datetime.now())
    })

    machines_owned.setdefault(phone, []).append(machine_id)

    ref = data.get('referrer')
    if ref and ref in users:
        users[ref]['balance'] += 17000
        users[ref]['referrals'] += 1

    return jsonify({"message": "Machine rented successfully"})

@app.route('/admin/all')
def admin():
    return jsonify({"users": users, "transactions": transactions})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
