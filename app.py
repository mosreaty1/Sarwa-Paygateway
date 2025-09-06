from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import hashlib
import secrets
import re
import requests
import threading
import time

app = Flask(__name__)
app.secret_key = 'sarwa_payment_secret_key_2024'

# MongoDB Connection
MONGO_URI = "mongodb://sarwa:sarwa123@ac-cwpuyax-shard-00-00.ovqkhu5.mongodb.net:27017,ac-cwpuyax-shard-00-01.ovqkhu5.mongodb.net:27017,ac-cwpuyax-shard-00-02.ovqkhu5.mongodb.net:27017/?replicaSet=atlas-nhnmy0-shard-0&ssl=true&authSource=admin"

try:
    client = MongoClient(MONGO_URI)
    db = client.sarwa_payments
    payments_collection = db.payments
    users_collection = db.users
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Crypto coins configuration with CoinGecko IDs
CRYPTO_COINS = {
    'BTC': {
        'name': 'Bitcoin', 
        'symbol': 'BTC', 
        'price': 111363.67,  # Default fallback price
        'icon': 'bitcoin', 
        'color': '#f7931a',
        'coingecko_id': 'bitcoin',
        'change_24h': 0
    },
    'ETH': {
        'name': 'Ethereum', 
        'symbol': 'ETH', 
        'price': 4415.51, 
        'icon': 'ethereum', 
        'color': '#627eea',
        'coingecko_id': 'ethereum',
        'change_24h': 0
    },
    'BNB': {
        'name': 'BNB', 
        'symbol': 'BNB', 
        'price': 587.25, 
        'icon': 'bnb', 
        'color': '#f3ba2f',
        'coingecko_id': 'binancecoin',
        'change_24h': 0
    },
    'ADA': {
        'name': 'Cardano', 
        'symbol': 'ADA', 
        'price': 0.735, 
        'icon': 'cardano', 
        'color': '#0033ad',
        'coingecko_id': 'cardano',
        'change_24h': 0
    },
    'SOL': {
        'name': 'Solana', 
        'symbol': 'SOL', 
        'price': 204.75, 
        'icon': 'solana', 
        'color': '#9945ff',
        'coingecko_id': 'solana',
        'change_24h': 0
    },
    'DOT': {
        'name': 'Polkadot', 
        'symbol': 'DOT', 
        'price': 8.45, 
        'icon': 'polkadot', 
        'color': '#e6007a',
        'coingecko_id': 'polkadot',
        'change_24h': 0
    },
}

def fetch_crypto_prices():
    """Fetch real-time crypto prices from CoinGecko API"""
    try:
        # Get all CoinGecko IDs
        coingecko_ids = [coin['coingecko_id'] for coin in CRYPTO_COINS.values()]
        ids_string = ','.join(coingecko_ids)
        
        # CoinGecko API endpoint (free tier)
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': ids_string,
            'vs_currencies': 'usd',
            'include_24hr_change': 'true'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        price_data = response.json()
        
        # Update prices in CRYPTO_COINS
        for symbol, coin_info in CRYPTO_COINS.items():
            coingecko_id = coin_info['coingecko_id']
            if coingecko_id in price_data:
                coin_info['price'] = price_data[coingecko_id]['usd']
                coin_info['change_24h'] = round(price_data[coingecko_id].get('usd_24h_change', 0), 2)
        
        print("✅ Crypto prices updated successfully!")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching crypto prices: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error fetching prices: {e}")
        return False

def price_updater():
    """Background thread to update prices every 60 seconds"""
    while True:
        fetch_crypto_prices()
        time.sleep(60)  # Update every minute

# Start price updater thread
price_thread = threading.Thread(target=price_updater, daemon=True)
price_thread.start()

# Fetch initial prices
fetch_crypto_prices()

def generate_payment_id():
    """Generate unique payment ID"""
    return f"PAY_{secrets.token_hex(8).upper()}"

def hash_card_number(card_number):
    """Hash card number for security"""
    return hashlib.sha256(card_number.encode()).hexdigest()

def validate_card_number(card_number):
    """Basic card number validation"""
    card_number = re.sub(r'\D', '', card_number)
    return len(card_number) >= 13 and len(card_number) <= 19

def validate_email(email):
    """Email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@app.route('/')
def index():
    """Home page with crypto selection"""
    return render_template('index.html', coins=CRYPTO_COINS)

@app.route('/api/crypto-prices')
def get_crypto_prices():
    """API endpoint to get current crypto prices"""
    try:
        prices = {}
        for symbol, coin in CRYPTO_COINS.items():
            prices[symbol] = {
                'price': coin['price'],
                'change_24h': coin['change_24h'],
                'symbol': coin['symbol'],
                'name': coin['name']
            }
        return jsonify({'success': True, 'prices': prices})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/payment/<coin_symbol>')
def payment_page(coin_symbol):
    """Payment page for selected crypto"""
    if coin_symbol not in CRYPTO_COINS:
        return redirect(url_for('index'))
    
    coin = CRYPTO_COINS[coin_symbol]
    return render_template('payment.html', coin=coin)

@app.route('/api/process_payment', methods=['POST'])
def process_payment():
    """Process payment API endpoint"""
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['email', 'full_name', 'card_number', 'expiry', 'cvv', 'coin_symbol', 'amount']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'Missing {field}'}), 400
        
        # Validate email
        if not validate_email(data['email']):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        
        # Validate card number
        if not validate_card_number(data['card_number']):
            return jsonify({'success': False, 'message': 'Invalid card number'}), 400
        
        # Validate coin
        if data['coin_symbol'] not in CRYPTO_COINS:
            return jsonify({'success': False, 'message': 'Invalid cryptocurrency'}), 400
        
        # Calculate investment details with current price
        coin = CRYPTO_COINS[data['coin_symbol']]
        amount_usd = float(data['amount'])
        crypto_amount = amount_usd / coin['price']
        
        # Generate payment record
        payment_id = generate_payment_id()
        payment_record = {
            'payment_id': payment_id,
            'email': data['email'],
            'full_name': data['full_name'],
            'card_hash': hash_card_number(data['card_number']),
            'card_last_four': data['card_number'][-4:],
            'coin_symbol': data['coin_symbol'],
            'coin_name': coin['name'],
            'coin_price': coin['price'],
            'amount_usd': amount_usd,
            'crypto_amount': crypto_amount,
            'status': 'completed',
            'created_at': datetime.utcnow(),
            'transaction_fee': amount_usd * 0.015,  # 1.5% fee
            'net_amount': amount_usd * 0.985
        }
        
        # Save to MongoDB
        payments_collection.insert_one(payment_record)
        
        return jsonify({
            'success': True, 
            'message': 'Payment processed successfully!',
            'payment_id': payment_id,
            'crypto_amount': round(crypto_amount, 8),
            'redirect_url': url_for('success', payment_id=payment_id)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Payment processing error: {str(e)}'}), 500

@app.route('/success/<payment_id>')
def success(payment_id):
    """Payment success page"""
    payment = payments_collection.find_one({'payment_id': payment_id})
    if not payment:
        return redirect(url_for('index'))
    
    return render_template('success.html', payment=payment)

@app.route('/api/payments')
def get_payments():
    """Get all payments (admin endpoint)"""
    try:
        payments = list(payments_collection.find().sort('created_at', -1).limit(50))
        for payment in payments:
            payment['_id'] = str(payment['_id'])
            payment['created_at'] = payment['created_at'].isoformat()
        
        return jsonify({'success': True, 'payments': payments})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard"""
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)