import os
from dotenv import load_dotenv

# Load .env file
load_dotenv('qr_flask_app/.env')

PLASTIC_BOTTLE_POINT = 1
ALUMINIUM_CAN_POINT = 7

# Get keys from .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:5000/auth/google/callback")

# Supabase Auth Configuration
SUPABASE_AUTH_CALLBACK_URL = "https://dvtbrhyjzsnftygioydt.supabase.co/auth/v1/callback"