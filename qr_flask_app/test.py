import qrcode
import secrets
import string
from urllib.parse import urlencode
from supabase import create_client

# Initialize Supabase client
supabase_url = "https://dvtbrhyjzsnftygioydt.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR2dGJyaHlqenNuZnR5Z2lveWR0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDUyNDUwMzUsImV4cCI6MjA2MDgyMTAzNX0.7bvlFfn8PKj0IupnMEKX4yUT2rEdk-VUOzARv3yMDew"
supabase = create_client(supabase_url, supabase_key)

# Raspberry Pi
def generate_session_id(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

# Raspberry Pi
def generate_qr_code(session_id, influx):
    base_identifier = "@SvenX-SmartBin"  # Replace with production domain if needed

    # Combine query parameters
    params = {'session_id': session_id}
    url = f"{base_identifier}:{urlencode(params)}"

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.show()

    # Upload session info
    upload_to_supabase(session_id, influx)

def upload_to_supabase(session_id, influx_data):
    try:
        data = {
            'bin_id': 1,
            'session_id': session_id,
            'influx': influx_data
        }
        response = supabase.table('waste_input_claim').insert(data).execute()
        print("Data uploaded:", response)
        return response
    except Exception as e:
        print("Upload failed:", e)
        return None

# --- Run the process ---
influx = {
    'plastic_bottle': 4,
    'can': 1
}
user_id = 4

session_id = generate_session_id()
generate_qr_code(session_id, influx)
