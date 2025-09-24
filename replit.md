# SmartBin QR Code Scanner Application

## Project Overview
This is a Flask-based web application for a smart waste collection system called "SmartBin". The application allows users to scan QR codes from smart waste bins to claim rewards based on the waste they've deposited (plastic bottles and cans).

## Key Features
- User authentication (login/signup)
- QR code scanning using camera
- Waste tracking (plastic bottles and cans)
- Points system (1 bottle = 1 point, 1 can = 6 points)
- Integration with Supabase database for data storage

## Architecture
- **Frontend**: HTML templates with embedded CSS and JavaScript
- **Backend**: Flask Python web framework
- **Database**: Supabase (PostgreSQL-based cloud database)
- **QR Code Scanning**: HTML5 QR Code library
- **Computer Vision**: OpenCV and PyZBar for QR processing

## Project Structure
```
qr_flask_app/
├── app.py              # Main Flask application
├── test.py             # Test script for QR generation
├── static/             # Static assets
│   └── html5-qrcode.min.js
└── templates/          # HTML templates
    ├── index.html      # Main scanner interface
    ├── login.html      # Login page
    └── signup.html     # Registration page
```

## Database Schema
The application uses Supabase with the following main tables:
- `user_data`: User accounts and authentication
- `waste_input_claim`: QR sessions and waste collection data

## Environment Setup
- Language: Python 3.11
- Host: 0.0.0.0 (configured for Replit environment)
- Port: 5000
- Dependencies managed via requirements.txt

## Recent Changes (2025-09-24)
- Configured Flask app to run on Replit environment (host 0.0.0.0, port 5000)
- Fixed potential unbound variable issue in QR scanning logic
- Added gunicorn for production deployment
- Configured autoscale deployment target for production

## Deployment Configuration
- **Development**: Flask development server with debug mode
- **Production**: Gunicorn WSGI server with autoscale deployment target
- **Port**: 5000 (frontend-only configuration)

## User Preferences
- No specific user preferences documented yet