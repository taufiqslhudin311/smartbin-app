# Vercel entry point for Flask app
import sys
import os

# Add the qr_flask_app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'qr_flask_app'))

from app import app

# Vercel expects the app to be available as 'app'
if __name__ == "__main__":
    app.run()
