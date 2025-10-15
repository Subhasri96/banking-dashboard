from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'credit' or 'debit'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 409

    hashed_pw = generate_password_hash(password)
    new_user = User(email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful"}), 201
"LOGIN PAGE"
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials/Not registered"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out"}), 200

@app.route('/add-transaction', methods=['POST'])
def add_transaction():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    amount = data['amount']
    description = data['description']
    date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    ttype = data['type']

    transaction = Transaction(
        amount=amount,
        description=description,
        date=date,
        type=ttype,
        user_id=session['user_id']
    )
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction added"}), 201

@app.route('/dashboard-data', methods=['GET'])
def dashboard_data():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session['user_id']
    transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date.desc()).all()

    balance = 0
    for t in transactions:
        balance += t.amount if t.type == 'credit' else -t.amount

    data = {
        "balance": round(balance, 2),
        "transactions": [
            {
                "amount": t.amount,
                "description": t.description,
                "date": t.date.strftime('%Y-%m-%d'),
                "type": t.type
            } for t in transactions
        ]
    }
    return jsonify(data)

@app.route('/hello', methods=['GET'])
def hello():
    return {"message": "Banking API operational. Ready to process requests."}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
