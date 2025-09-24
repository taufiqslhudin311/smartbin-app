from flask import Flask, request, render_template, redirect, url_for, jsonify, session, flash
from supabase import create_client
import os
from urllib.parse import parse_qs, urlencode
import requests
import json

from config import (SUPABASE_URL, SUPABASE_KEY, PLASTIC_BOTTLE_POINT, ALUMINIUM_CAN_POINT,
                   GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, SUPABASE_AUTH_CALLBACK_URL)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_waste_statistics(user_id):
    try:
        # Get all waste input claims for the user
        response = supabase.table("waste_input_claim") \
            .select("influx") \
            .eq("user_id", user_id) \
            .execute()
        
        if not response.data:
            return {"can": 0, "plastic_bottle": 0, "total_points": 0}
        
        # Sum up all the waste items
        total_cans = 0
        total_plastic_bottles = 0
        
        for claim in response.data:
            influx = claim.get('influx', {})
            total_cans += influx.get('can', 0)
            total_plastic_bottles += influx.get('plastic_bottle', 0)
        
        # Calculate total points (1 bottle = 1 point, 1 can = 6 points)
        total_points = PLASTIC_BOTTLE_POINT * total_plastic_bottles + (ALUMINIUM_CAN_POINT * total_cans)
        
        return {
            "can": total_cans,
            "plastic_bottle": total_plastic_bottles,
            "total_points": total_points
        }
    except Exception as e:
        print(f"Error getting waste statistics: {str(e)}")
        return {"can": 0, "plastic_bottle": 0, "total_points": 0}

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('scan_page'))
    return render_template('landing.html')

@app.route('/health')
def health_check():
    """Simple health check endpoint for deployment testing"""
    return jsonify({
        'status': 'healthy',
        'message': 'SmartBin Flask app is running',
        'version': '1.0.0'
    })

@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/scan', methods=['GET'])
def scan_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get waste statistics for the current user
    waste_stats = get_waste_statistics(session['user_id'])
    return render_template('index.html', waste_stats=waste_stats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            # Query user from Supabase with email and password match
            response = supabase.table('user_data').select('*').eq('email', email).eq('password', password).execute()
            
            if response.data and len(response.data) > 0:
                user = response.data[0]
                session['user_id'] = user['user_id']  # Store user_id in session
                session['email'] = user['email']
                session['first_name'] = user['first_name']
                session['last_name'] = user['last_name']
                flash('Login successful!', 'success')
                return redirect(url_for('scan_page'))  # Redirect to scanner page
            else:
                flash('Invalid email or password', 'error')
        except Exception as e:
            flash('Error during login', 'error')
            print(f"Login error: {str(e)}")
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        
        try:
            # Check if email already exists
            response = supabase.table('user_data').select('*').eq('email', email).execute()
            
            if response.data and len(response.data) > 0:
                flash('Email already exists', 'error')
                return redirect(url_for('signup'))
            
            # Insert new user into Supabase
            user_data = {
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'password': password
            }
            
            response = supabase.table('user_data').insert(user_data).execute()
            
            if response.data:
                flash('Account created successfully! Please login.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Error creating account', 'error')
                
        except Exception as e:
            flash('Error during signup', 'error')
            print(f"Signup error: {str(e)}")
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/auth/google')
def google_auth():
    """Initiate Google OAuth flow"""
    if not GOOGLE_CLIENT_ID:
        flash('Google OAuth not configured', 'error')
        return redirect(url_for('login'))
    
    # Google OAuth URL parameters
    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'scope': 'openid email profile',
        'response_type': 'code',
        'access_type': 'offline',
        'prompt': 'consent'
    }
    
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return redirect(auth_url)

@app.route('/auth/google/callback')
def google_callback():
    """Handle Google OAuth callback"""
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        flash(f'Google OAuth error: {error}', 'error')
        return redirect(url_for('login'))
    
    if not code:
        flash('No authorization code received', 'error')
        return redirect(url_for('login'))
    
    try:
        # Exchange code for tokens
        token_data = {
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': GOOGLE_REDIRECT_URI
        }
        
        response = requests.post('https://oauth2.googleapis.com/token', data=token_data)
        token_response = response.json()
        
        if 'access_token' not in token_response:
            flash('Failed to get access token from Google', 'error')
            return redirect(url_for('login'))
        
        access_token = token_response['access_token']
        
        # Get user info from Google
        user_info_response = requests.get(
            f'https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}'
        )
        user_info = user_info_response.json()
        
        if 'email' not in user_info:
            flash('Failed to get user information from Google', 'error')
            return redirect(url_for('login'))
        
        # Check if user exists in Supabase, if not create them
        email = user_info['email']
        first_name = user_info.get('given_name', '')
        last_name = user_info.get('family_name', '')
        
        # Query user from Supabase
        response = supabase.table('user_data').select('*').eq('email', email).execute()
        
        if response.data and len(response.data) > 0:
            # User exists, log them in
            user = response.data[0]
            session['user_id'] = user['user_id']
            session['email'] = user['email']
            session['first_name'] = user['first_name']
            session['last_name'] = user['last_name']
            session['auth_provider'] = 'google'
        else:
            # User doesn't exist, create new user
            user_data = {
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'password': None,  # No password for OAuth users
                'auth_provider': 'google'
            }
            
            response = supabase.table('user_data').insert(user_data).execute()
            
            if response.data:
                user = response.data[0]
                session['user_id'] = user['user_id']
                session['email'] = user['email']
                session['first_name'] = user['first_name']
                session['last_name'] = user['last_name']
                session['auth_provider'] = 'google'
            else:
                flash('Error creating user account', 'error')
                return redirect(url_for('login'))
        
        flash('Successfully logged in with Google!', 'success')
        return redirect(url_for('scan_page'))
        
    except Exception as e:
        flash(f'Error during Google authentication: {str(e)}', 'error')
        print(f"Google OAuth error: {str(e)}")
        return redirect(url_for('login'))

@app.route('/api/scan', methods=['POST'])
def scan():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
        
    data = request.json
    if data and 'qr_data' in data:
        qr_data = data['qr_data']
        
        # Check if QR code matches the expected format
        if not qr_data.startswith('@SvenX-SmartBin:'):
            return jsonify({'success': False, 'message': 'Invalid QR code format'}), 400
            
        try:
            # Extract session_id from QR code
            # Format: @SvenX-SmartBin:session_id=xxx
            params = parse_qs(qr_data.split(':', 1)[1])
            session_id = params.get('session_id', [None])[0]
            
            if not session_id:
                return jsonify({'success': False, 'message': 'No session ID found in QR code'}), 400
            
            # Check if session has already been claimed
            check_response = supabase.table("waste_input_claim") \
                .select("user_id, influx") \
                .eq("session_id", session_id) \
                .execute()
            
            if check_response.data and len(check_response.data) > 0:
                if check_response.data[0].get('user_id') is not None:
                    return jsonify({
                        'success': False, 
                        'message': 'Reward Already Claimed'
                    }), 400
                
                # Calculate session points
                influx = check_response.data[0].get('influx', {})
                session_points = influx.get('plastic_bottle', 0) + (6 * influx.get('can', 0))
            else:
                session_points = 0
            
            # Update the waste_input_claim table with user_id
            response = supabase.table("waste_input_claim") \
                .update({"user_id": session['user_id']}) \
                .eq("session_id", session_id) \
                .execute()
            
            if response.data:
                # Get updated waste statistics
                waste_stats = get_waste_statistics(session['user_id'])
                return jsonify({
                    'success': True, 
                    'message': 'QR code scanned and processed successfully',
                    'session_id': session_id,
                    'waste_stats': waste_stats,
                    'session_points': session_points
                })
            else:
                return jsonify({'success': False, 'message': 'Failed to update waste input claim'}), 500
                
        except Exception as e:
            print(f"Error processing QR code: {str(e)}")
            return jsonify({'success': False, 'message': 'Error processing QR code'}), 500
            
    return jsonify({'success': False, 'message': 'No QR data received'}), 400

# For Vercel deployment
app.debug = False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
