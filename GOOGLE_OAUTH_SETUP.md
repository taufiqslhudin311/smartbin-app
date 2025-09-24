# Google OAuth Setup Guide for SmartBin App

## Overview
This guide will help you set up Google OAuth authentication with Supabase integration for your SmartBin application.

## Prerequisites
- Google Cloud Console account
- Supabase project
- Python environment with Flask

## Step 1: Google Cloud Console Setup

### 1.1 Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API

### 1.2 Configure OAuth Consent Screen
1. Navigate to "APIs & Services" > "OAuth consent screen"
2. Choose "External" user type
3. Fill in the required information:
   - App name: SmartBin
   - User support email: your-email@example.com
   - Developer contact: your-email@example.com
4. Add scopes: `email`, `profile`, `openid`
5. Add test users (for development)

### 1.3 Create OAuth 2.0 Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Web application"
4. Add authorized redirect URIs:
   - Development: `http://localhost:5000/auth/google/callback`
   - Production: `https://yourdomain.com/auth/google/callback`
5. Copy the Client ID and Client Secret

## Step 2: Supabase Configuration

### 2.1 Enable Google Provider
1. Go to your Supabase dashboard
2. Navigate to "Authentication" > "Providers"
3. Enable Google provider
4. Add your Google OAuth credentials:
   - Client ID: (from Google Cloud Console)
   - Client Secret: (from Google Cloud Console)
5. Set the redirect URL to: `https://dvtbrhyjzsnftygioydt.supabase.co/auth/v1/callback`

## Step 3: Environment Variables

Create a `.env` file in your `qr_flask_app` directory with the following variables:

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:5000/auth/google/callback
```

## Step 4: Database Schema Update

You may need to update your `user_data` table in Supabase to include an `auth_provider` column:

```sql
ALTER TABLE user_data ADD COLUMN auth_provider VARCHAR(50) DEFAULT 'email';
```

## Step 5: Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Step 6: Testing

1. Start your Flask application:
   ```bash
   python qr_flask_app/app.py
   ```

2. Navigate to `http://localhost:5000/login`
3. Click "Continue with Google"
4. Complete the OAuth flow
5. Verify that you're redirected to the scan page

## Features Added

### 1. Google OAuth Integration
- **Route**: `/auth/google` - Initiates Google OAuth flow
- **Route**: `/auth/google/callback` - Handles OAuth callback
- **Authentication**: Automatic user creation/login via Google

### 2. Enhanced Login Page
- Google OAuth button with proper styling
- Visual divider between OAuth and traditional login
- Responsive design

### 3. User Management
- Automatic user creation for new Google users
- Session management for OAuth users
- Integration with existing user data structure

## Security Considerations

1. **Environment Variables**: Never commit `.env` files to version control
2. **HTTPS**: Use HTTPS in production for OAuth redirects
3. **Client Secrets**: Keep Google Client Secret secure
4. **Session Security**: Flask sessions are used for user state management

## Troubleshooting

### Common Issues:

1. **"Google OAuth not configured"**
   - Ensure `GOOGLE_CLIENT_ID` is set in your `.env` file

2. **"Invalid redirect URI"**
   - Check that the redirect URI in Google Console matches your `GOOGLE_REDIRECT_URI`

3. **"Failed to get access token"**
   - Verify your Google Client Secret is correct
   - Check that the OAuth consent screen is properly configured

4. **Database errors**
   - Ensure your Supabase credentials are correct
   - Check that the `user_data` table exists and has the required columns

## Production Deployment

For production deployment:

1. Update `GOOGLE_REDIRECT_URI` to your production domain
2. Add your production domain to Google OAuth authorized redirect URIs
3. Use environment variables or secure configuration management
4. Enable HTTPS for your application

## Support

If you encounter issues:
1. Check the Flask application logs for error messages
2. Verify all environment variables are correctly set
3. Test the OAuth flow step by step
4. Ensure your Google Cloud Console and Supabase configurations match
