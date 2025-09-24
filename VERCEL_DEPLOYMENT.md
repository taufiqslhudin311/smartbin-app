# Vercel Deployment Guide for SmartBin Flask App

## 🚀 Quick Fix for Your Current Issue

Your Flask app failed to deploy on Vercel because it needs proper configuration. I've added the necessary files:

### Files Added:
1. `vercel.json` - Vercel configuration for Flask
2. `api/index.py` - Entry point for Vercel
3. Updated Flask app for production

## 📋 Step-by-Step Deployment

### 1. **Set Environment Variables in Vercel**

Go to your Vercel dashboard → Project Settings → Environment Variables and add:

```
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
GOOGLE_REDIRECT_URI=https://your-vercel-domain.vercel.app/auth/google/callback
```

### 2. **Update Google OAuth Settings**

In Google Cloud Console, add your Vercel domain to authorized redirect URIs:
- `https://your-vercel-domain.vercel.app/auth/google/callback`

### 3. **Push Updated Code**

```bash
git add .
git commit -m "feat: Add Vercel deployment configuration"
git push origin main
```

### 4. **Redeploy on Vercel**

Vercel should automatically redeploy when you push to main branch.

## 🔧 Configuration Files Explained

### `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "qr_flask_app/app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "qr_flask_app/app.py"
    }
  ]
}
```

### `api/index.py`
Entry point that imports your Flask app for Vercel's serverless functions.

## 🌐 Alternative Deployment Options

If Vercel continues to have issues, consider these alternatives:

### **Option A: Railway (Recommended for Flask)**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### **Option B: Render**
1. Connect your GitHub repo to Render
2. Choose "Web Service"
3. Build command: `pip install -r requirements.txt`
4. Start command: `python qr_flask_app/app.py`

### **Option C: PythonAnywhere**
1. Upload your code
2. Create a web app
3. Configure WSGI file to point to your Flask app

## ⚠️ Common Vercel Issues with Flask

1. **Cold Starts**: Serverless functions have cold start delays
2. **Session Storage**: Flask sessions might not persist across requests
3. **File System**: Limited file system access in serverless environment

## 🔍 Debugging Your Current Deployment

To check what's happening:

1. **Check Vercel Function Logs**:
   - Go to Vercel dashboard → Your project → Functions tab
   - Look for error logs

2. **Test API Endpoints**:
   ```bash
   curl https://your-vercel-domain.vercel.app/
   ```

3. **Check Build Logs**:
   - Look for Python import errors
   - Check if all dependencies are installed

## 🎯 Expected Behavior After Fix

After applying these changes and redeploying:

1. **Root URL** (`/`) should show your landing page
2. **Login URL** (`/login`) should show login form with Google OAuth
3. **Google OAuth** should redirect to your Vercel domain

## 📞 Need Help?

If you're still getting 404 errors after these changes:

1. Check Vercel function logs for Python errors
2. Verify all environment variables are set
3. Test individual routes
4. Consider switching to Railway or Render for easier Flask deployment

The main issue was missing Vercel configuration - your Flask app is perfectly fine, it just needed the right deployment setup!
