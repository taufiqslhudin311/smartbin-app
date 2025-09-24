import os
from dotenv import load_dotenv

# Load .env file
load_dotenv('qr_flask_app/.env')

PLASTIC_BOTTLE_POINT = 1
ALUMINIUM_CAN_POINT = 7

# Get keys from .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
