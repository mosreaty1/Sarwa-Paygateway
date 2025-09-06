# Sarwa - Professional Cryptocurrency Investment Platform

A modern, professional-grade web application for cryptocurrency investment with real-time market data, secure payment processing, and comprehensive admin dashboard.

## Features

### 🚀 Core Features
- **Real-time Cryptocurrency Markets**: Live price updates for Bitcoin, Ethereum, BNB, Cardano, Solana, and Polkadot
- **Interactive Price Charts**: Dynamic charts with simulated market data
- **Secure Payment Processing**: Complete investment workflow with card validation
- **Admin Dashboard**: Comprehensive analytics and payment monitoring
- **Responsive Design**: Mobile-first design with modern UI/UX

### 💹 Supported Cryptocurrencies
- Bitcoin (BTC)
- Ethereum (ETH)
- BNB (BNB)
- Cardano (ADA)
- Solana (SOL)
- Polkadot (DOT)

### 🔐 Security Features
- Card number hashing for secure storage
- Input validation and sanitization
- HTTPS-ready configuration
- MongoDB secure connection

## Technology Stack

### Backend
- **Flask**: Python web framework
- **PyMongo**: MongoDB driver for Python
- **MongoDB Atlas**: Cloud database solution
- **CoinGecko API**: Real-time cryptocurrency price data

### Frontend
- **HTML5/CSS3**: Modern semantic markup and styling
- **JavaScript ES6+**: Interactive functionality
- **Chart.js**: Dynamic price charts
- **Font Awesome**: Professional iconography
- **Inter Font**: Modern typography

### Dependencies
```
Flask==2.3.3
pymongo==4.5.0
python-dotenv==1.0.0
Werkzeug==2.3.7
dnspython==2.4.2
certifi==2023.7.22
requests==2.31.0
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MongoDB Atlas account (or local MongoDB installation)
- Internet connection for real-time price data

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/sarwa.git
cd sarwa
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
MONGO_URI=your_mongodb_connection_string
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

### 5. Database Setup
The application automatically creates necessary collections in MongoDB:
- `payments`: Stores payment transactions
- `users`: User management (future implementation)

### 6. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## API Endpoints

### Public Endpoints
- `GET /` - Home page with cryptocurrency markets
- `GET /payment/<coin_symbol>` - Payment page for specific cryptocurrency
- `GET /success/<payment_id>` - Payment confirmation page

### API Endpoints
- `GET /api/crypto-prices` - Get current cryptocurrency prices
- `POST /api/process_payment` - Process investment payment
- `GET /api/payments` - Get all payments (admin)

### Admin Endpoints
- `GET /admin` - Admin dashboard with analytics

## Project Structure

```
sarwa/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Home page with crypto markets
│   ├── payment.html      # Payment processing form
│   ├── success.html      # Payment confirmation
│   └── admin.html        # Admin dashboard
├── static/               # Static assets (if any)
└── README.md            # This file
```

## Features Overview

### Home Page (`/`)
- Live cryptocurrency market data
- Interactive price charts
- Real-time price updates every 1.5 seconds
- Responsive grid layout for crypto cards
- Investment amount calculator

### Payment Processing (`/payment/<symbol>`)
- Secure payment form with validation
- Real-time investment calculation
- Processing fee display (1.5%)
- Card number validation
- Cryptocurrency amount calculation

### Admin Dashboard (`/admin`)
- Total revenue and payment statistics
- Unique investor count
- Recent payments table with search
- Real-time data refresh
- Payment status monitoring

### Success Page (`/success/<payment_id>`)
- Payment confirmation details
- Transaction receipt
- Print functionality
- Investment summary

## Database Schema

### Payments Collection
```javascript
{
  "_id": ObjectId,
  "payment_id": "PAY_XXXXXXXX",
  "email": "user@example.com",
  "full_name": "John Doe",
  "card_hash": "hashed_card_number",
  "card_last_four": "1234",
  "coin_symbol": "BTC",
  "coin_name": "Bitcoin",
  "coin_price": 45000.00,
  "amount_usd": 1000.00,
  "crypto_amount": 0.02222222,
  "transaction_fee": 15.00,
  "net_amount": 985.00,
  "status": "completed",
  "created_at": ISODate
}
```

## Security Considerations

1. **Card Data Protection**: Card numbers are hashed using SHA-256
2. **Input Validation**: All user inputs are validated server-side
3. **Secure Database**: MongoDB connection uses SSL/TLS encryption
4. **Environment Variables**: Sensitive data stored in environment variables
5. **HTTPS Ready**: Application configured for HTTPS deployment

## Configuration

### MongoDB Configuration
Update the `MONGO_URI` in `app.py` or use environment variables:
```python
MONGO_URI = "your_mongodb_connection_string"
```

### Cryptocurrency Configuration
Modify `CRYPTO_COINS` dictionary in `app.py` to add/remove cryptocurrencies:
```python
CRYPTO_COINS = {
    'BTC': {
        'name': 'Bitcoin',
        'symbol': 'BTC',
        'coingecko_id': 'bitcoin',
        'color': '#f7931a',
        # ... other properties
    }
}
```

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python app.py
```

### Code Structure
- **Flask Routes**: Main application routes in `app.py`
- **Templates**: Jinja2 templates in `templates/` directory
- **Static Assets**: CSS and JavaScript embedded in templates
- **Database Models**: MongoDB collections with validation

## Deployment

### Environment Setup
1. Set production environment variables
2. Update MongoDB connection for production
3. Configure HTTPS certificates
4. Set appropriate CORS headers if needed

### Production Considerations
- Use a production WSGI server (Gunicorn, uWSGI)
- Configure reverse proxy (Nginx, Apache)
- Enable logging and monitoring
- Set up backup strategies for MongoDB
- Implement rate limiting for API endpoints

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


alsariti1@gmail.com


## Disclaimer

This is a demonstration application for educational purposes. Do not use this application for actual cryptocurrency investments without proper security audits and compliance with financial regulations.

---

**Built with ❤️ using Flask, MongoDB, and modern web technologies**
