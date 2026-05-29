import os
import json
from flask import Flask, jsonify, request, render_template

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
DATA_FILE = os.path.join(DATA_DIR, 'data.json')

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)

# Default data state representing realistic spending
DEFAULT_DATA = {
    "income": 5000.00,
    "budget": 1500.00,
    "savingsGoal": 0.0,
    "categoryLimits": {},
    "recurring": [],
    "transactions": [
        {
            "id": 1,
            "category": "Food",
            "emoji": "🍔",
            "description": "Organic Grocery Store",
            "amount": 120.50,
            "tags": ["personal", "household"],
            "date": "2026-05-25"
        },
        {
            "id": 2,
            "category": "Utilities",
            "emoji": "💡",
            "description": "High-speed Internet & Power",
            "amount": 85.00,
            "tags": ["household"],
            "date": "2026-05-24"
        },
        {
            "id": 3,
            "category": "Transport",
            "emoji": "🚗",
            "description": "Gas Station & Highway Tolls",
            "amount": 45.00,
            "tags": ["vacation"],
            "date": "2026-05-23"
        },
        {
            "id": 4,
            "category": "Food",
            "emoji": "🍔",
            "description": "Premium Sushi & Cocktails",
            "amount": 95.00,
            "tags": ["vacation", "leisure"],
            "date": "2026-05-22"
        },
        {
            "id": 5,
            "category": "Entertainment",
            "emoji": "🍿",
            "description": "Netflix Premium & Spotify",
            "amount": 29.99,
            "tags": ["personal", "subscriptions"],
            "date": "2026-05-20"
        },
        {
            "id": 6,
            "category": "Shopping",
            "emoji": "🛍️",
            "description": "Designer Leather Sneakers",
            "amount": 180.00,
            "tags": ["leisure"],
            "date": "2026-05-18"
        }
    ]
}

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Safe migration of new state fields
            updated = False
            if 'savingsGoal' not in data:
                data['savingsGoal'] = 0.0
                updated = True
            if 'categoryLimits' not in data:
                data['categoryLimits'] = {}
                updated = True
            if 'recurring' not in data:
                data['recurring'] = []
                updated = True
            if updated:
                save_data(data)
            return data
    except Exception:
        return DEFAULT_DATA

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_all_data():
    return jsonify(load_data())

@app.route('/api/income', methods=['POST'])
def update_income():
    req_data = request.get_json()
    if not req_data or 'income' not in req_data:
        return jsonify({"error": "Invalid payload"}), 400
    
    try:
        new_income = float(req_data['income'])
        if new_income < 0:
            raise ValueError
    except ValueError:
        return jsonify({"error": "Income must be a positive number"}), 400
    
    data = load_data()
    data['income'] = new_income
    save_data(data)
    return jsonify(data)

@app.route('/api/budget', methods=['POST'])
def update_budget():
    req_data = request.get_json()
    if not req_data or 'budget' not in req_data:
        return jsonify({"error": "Invalid payload"}), 400
    
    try:
        new_budget = float(req_data['budget'])
        if new_budget < 0:
            raise ValueError
    except ValueError:
        return jsonify({"error": "Budget must be a positive number"}), 400
    
    data = load_data()
    data['budget'] = new_budget
    save_data(data)
    return jsonify(data)

@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    req_data = request.get_json()
    required = ['category', 'emoji', 'description', 'amount', 'date']
    if not req_data or not all(k in req_data for k in required):
        return jsonify({"error": "Missing transaction details"}), 400
    
    try:
        amount = float(req_data['amount'])
        if amount <= 0:
            raise ValueError
    except ValueError:
        return jsonify({"error": "Amount must be a positive number"}), 400
    
    data = load_data()
    
    # Generate new unique ID
    manual_ids = [int(t['id']) for t in data['transactions'] if isinstance(t['id'], int) or (isinstance(t['id'], str) and str(t['id']).isdigit())]
    new_id = max(manual_ids, default=0) + 1
    
    new_tx = {
        "id": new_id,
        "category": req_data['category'],
        "emoji": req_data['emoji'],
        "description": req_data['description'],
        "amount": amount,
        "tags": req_data.get('tags', []),
        "date": req_data['date']
    }
    
    data['transactions'].append(new_tx)
    save_data(data)
    return jsonify(data), 201

@app.route('/api/transactions/<int:tx_id>', methods=['PUT'])
def update_transaction(tx_id):
    req_data = request.get_json()
    if not req_data:
        return jsonify({"error": "Invalid payload"}), 400
        
    data = load_data()
    found_idx = -1
    for idx, tx in enumerate(data['transactions']):
        if tx['id'] == tx_id:
            found_idx = idx
            break
            
    if found_idx == -1:
        return jsonify({"error": "Transaction not found"}), 404
        
    tx = data['transactions'][found_idx]
    if 'category' in req_data:
        tx['category'] = req_data['category']
    if 'emoji' in req_data:
        tx['emoji'] = req_data['emoji']
    if 'description' in req_data:
        tx['description'] = req_data['description']
    if 'amount' in req_data:
        try:
            amount = float(req_data['amount'])
            if amount <= 0:
                raise ValueError
            tx['amount'] = amount
        except ValueError:
            return jsonify({"error": "Amount must be a positive number"}), 400
    if 'tags' in req_data:
        tx['tags'] = req_data['tags']
    if 'date' in req_data:
        tx['date'] = req_data['date']
        
    data['transactions'][found_idx] = tx
    save_data(data)
    return jsonify(data)

@app.route('/api/transactions/<int:tx_id>', methods=['DELETE'])
def delete_transaction(tx_id):
    data = load_data()
    initial_len = len(data['transactions'])
    data['transactions'] = [t for t in data['transactions'] if t['id'] != tx_id]
    
    if len(data['transactions']) == initial_len:
        return jsonify({"error": "Transaction not found"}), 404
        
    save_data(data)
    return jsonify(data)

@app.route('/api/savings-goal', methods=['POST'])
def update_savings_goal():
    req_data = request.get_json()
    if not req_data or 'savingsGoal' not in req_data:
        return jsonify({"error": "Invalid payload"}), 400
    
    try:
        new_goal = float(req_data['savingsGoal'])
        if new_goal < 0:
            raise ValueError
    except ValueError:
        return jsonify({"error": "Savings goal must be a positive number"}), 400
        
    data = load_data()
    data['savingsGoal'] = new_goal
    save_data(data)
    return jsonify(data)

@app.route('/api/category-limits', methods=['POST'])
def update_category_limits():
    req_data = request.get_json()
    if not req_data or 'categoryLimits' not in req_data:
        return jsonify({"error": "Invalid payload"}), 400
        
    data = load_data()
    data['categoryLimits'] = req_data['categoryLimits']
    save_data(data)
    return jsonify(data)

@app.route('/api/recurring', methods=['POST'])
def update_recurring():
    req_data = request.get_json()
    if not req_data or 'recurring' not in req_data:
        return jsonify({"error": "Invalid payload"}), 400
        
    data = load_data()
    data['recurring'] = req_data['recurring']
    save_data(data)
    return jsonify(data)

@app.route('/api/sync', methods=['POST'])
def sync_data():
    req_data = request.get_json()
    if not req_data:
        return jsonify({"error": "Invalid payload"}), 400
        
    data = load_data()
    if 'income' in req_data:
        data['income'] = float(req_data['income'])
    if 'budget' in req_data:
        data['budget'] = float(req_data['budget'])
    if 'transactions' in req_data:
        data['transactions'] = req_data['transactions']
    if 'savingsGoal' in req_data:
        data['savingsGoal'] = float(req_data['savingsGoal'])
    if 'categoryLimits' in req_data:
        data['categoryLimits'] = req_data['categoryLimits']
    if 'recurring' in req_data:
        data['recurring'] = req_data['recurring']
        
    save_data(data)
    return jsonify(data)

@app.route('/sw.js')
def serve_sw():
    return app.send_static_file('sw.js')

@app.route('/manifest.json')
def serve_manifest():
    return app.send_static_file('manifest.json')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
