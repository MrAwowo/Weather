# 📱 Mobile Installation Guide

Install the Weather Prediction app on your phone as a Progressive Web App (PWA)!

## What is a PWA?

A Progressive Web App works like a native app but runs in your browser:
- ✅ Install on home screen
- ✅ Works offline (with cached data)
- ✅ Full-screen experience
- ✅ Fast and responsive
- ✅ No App Store needed
- ✅ Updates automatically

---

## 📥 Installation Instructions

### iPhone/iPad (iOS/iPadOS)

1. **Open Safari** (must use Safari, not Chrome)
2. Navigate to your app URL (e.g., `http://your-server:8501`)
3. Tap the **Share** button (square with arrow pointing up)
4. Scroll down and tap **"Add to Home Screen"**
5. Edit the name if you want (e.g., "Weather")
6. Tap **"Add"** in the top right

**Icon will appear on your home screen!** 🎉

**Tips:**
- Works best on iOS 16.4+
- First load requires internet, then works offline
- Swipe down to refresh data

---

### Android (Chrome)

1. **Open Chrome** browser
2. Navigate to your app URL (e.g., `http://your-server:8501`)
3. Tap the **three dots** menu (⋮) in top right
4. Tap **"Add to Home screen"** or **"Install app"**
5. Confirm by tapping **"Add"** or **"Install"**

**Alternative method:**
- Chrome may show a banner at the bottom saying "Add Weather Predict to Home screen"
- Tap **"Add"** on the banner

**Icon will appear on your home screen!** 🎉

**Tips:**
- Works on Android 5.0+
- First load requires internet
- Pull down to refresh

---

### Android (Samsung Internet)

1. Open **Samsung Internet** browser
2. Navigate to your app URL
3. Tap the **three lines** menu
4. Tap **"Add page to"** → **"Home screen"**
5. Tap **"Add"**

---

### Android (Firefox)

1. Open **Firefox** browser
2. Navigate to your app URL
3. Tap the **three dots** menu
4. Tap **"Install"**
5. Confirm installation

---

## 🌐 Deploying the App

To make your app accessible from your phone, you need to deploy it. Here are your options:

### Option 1: Local Network (Same WiFi)

**Quick and Free - Perfect for Personal Use**

1. **Find your computer's IP address:**

   **On Mac:**
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```

   **On Linux:**
   ```bash
   hostname -I
   ```

   **On Windows:**
   ```bash
   ipconfig
   ```

   You'll see something like `192.168.1.100`

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

3. **On your phone** (connected to same WiFi):
   - Open browser
   - Go to: `http://192.168.1.100:8501`
   - Follow installation instructions above

**Pros:**
- ✅ Free
- ✅ Fast
- ✅ Private

**Cons:**
- ❌ Only works on same WiFi
- ❌ Computer must be running

---

### Option 2: Cloud Deployment (Internet Access)

**Deploy to the cloud for access anywhere:**

#### A) Streamlit Cloud (Easiest, Free)

1. **Push code to GitHub** (already done!)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository: `MrAwowo/Weather`
6. Main file: `app.py`
7. Click "Deploy"

**Your app URL:** `https://your-app-name.streamlit.app`

**Pros:**
- ✅ Completely free
- ✅ HTTPS (secure)
- ✅ Custom domain option
- ✅ Auto-updates from GitHub

**Cons:**
- ❌ Public by default
- ❌ Resource limits on free tier

---

#### B) Railway (Easy, Free Tier)

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `MrAwowo/Weather`
5. Railway auto-detects Streamlit
6. Add environment variables if needed
7. Deploy

**Your app URL:** `https://your-app.railway.app`

---

#### C) Render (Free Tier Available)

1. Go to [render.com](https://render.com)
2. Sign up and connect GitHub
3. Click "New" → "Web Service"
4. Select `MrAwowo/Weather`
5. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. Click "Create Web Service"

---

#### D) Heroku (Paid, but reliable)

1. Create `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "[server]
   headless = true
   port = $PORT
   enableCORS = false
   " > ~/.streamlit/config.toml
   ```

3. Deploy to Heroku:
   ```bash
   heroku create your-weather-app
   git push heroku main
   ```

---

### Option 3: ngrok (Quick Testing)

**Perfect for showing the app to friends temporarily:**

1. **Install ngrok:**
   - Download from [ngrok.com](https://ngrok.com)
   - Or: `brew install ngrok` (Mac)

2. **Run your app:**
   ```bash
   streamlit run app.py
   ```

3. **In another terminal, run ngrok:**
   ```bash
   ngrok http 8501
   ```

4. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)
5. **Open on your phone** and install as PWA

**Pros:**
- ✅ Super fast setup
- ✅ HTTPS included
- ✅ Works from anywhere

**Cons:**
- ❌ URL changes each time (free tier)
- ❌ Temporary (8 hours max on free tier)
- ❌ Requires computer running

---

## 🎯 Recommended Setup

**For Personal Use:**
```
1. Local Network (same WiFi) - for daily use
2. Streamlit Cloud - for access anywhere
```

**For Sharing with Friends:**
```
Streamlit Cloud or Railway - permanent, free, easy
```

**For Production:**
```
Render or Railway with custom domain
```

---

## 📲 After Installation

### Test the PWA Features

1. **Offline Mode:**
   - Open the app
   - Turn off WiFi/data
   - App should still display (cached version)

2. **Full Screen:**
   - No browser UI
   - Looks like native app
   - Swipe gestures work

3. **Home Screen Icon:**
   - Tap to open
   - Launches full-screen
   - Appears in app switcher

### Using the App

1. **Current Weather:**
   - Enter city name
   - Tap "Fetch Current Weather"
   - View conditions

2. **Predictions:**
   - Tap "Generate Predictions"
   - View 7-day forecast
   - Scroll through prediction cards

3. **Analytics:**
   - View charts
   - See temperature distributions
   - Check Markov probabilities

4. **Offline:**
   - Last viewed data stays cached
   - Predictions can be viewed offline
   - Need internet for new data

---

## 🔧 Troubleshooting

### "Cannot connect to server"
- Check WiFi connection
- Verify IP address is correct
- Ensure computer is on same network
- Check firewall settings

### "Add to Home Screen not appearing"
- **iOS:** Must use Safari browser
- **Android:** Use Chrome or Samsung Internet
- Make sure site is HTTPS (for cloud deployments)
- Try force refresh (pull down)

### App won't load
- Check internet connection
- Clear browser cache
- Reinstall PWA
- Verify server is running

### Predictions not working
- Needs internet for historical data
- Check Open-Meteo API status
- Try different city name
- Check browser console for errors

---

## 🚀 Performance Tips

### For Best Mobile Experience:

1. **Use WiFi** when possible (faster than cellular)
2. **Close other apps** for better performance
3. **Update regularly** (PWAs auto-update)
4. **Cache data** by using the app regularly
5. **Bookmark favorite cities** in browser

### Battery Optimization:

- Don't keep app open in background
- Fetch predictions once per day
- Disable auto-refresh if added
- Use dark mode (if your device supports it)

---

## 📊 Data Usage

**Approximate data usage:**
- Initial load: ~2-5 MB
- Fetch current weather: ~10-50 KB
- Generate predictions: ~100-500 KB (historical data)
- Charts/visualizations: ~50-100 KB

**Total:** Very light! ~3-6 MB per day with normal use.

---

## 🎨 Customization

### Change Theme (for developers)

Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#2193b0"  # Change to your color
backgroundColor = "#ffffff"
```

### Adjust for Your Screen

The app automatically adapts to:
- Small phones (< 375px)
- Regular phones (375-768px)
- Tablets (768-1024px)
- Desktop (> 1024px)

---

## ✨ What's Next?

After installing as PWA, you can:

1. ✅ Use like a native app
2. ✅ Add to favorites/bookmarks
3. ✅ Share with friends
4. ✅ Access from anywhere (if cloud deployed)
5. ✅ Get automatic updates

---

## 🆘 Need Help?

- Check the main [README.md](README.md)
- Review [SETUP.md](SETUP.md) for deployment details
- Open an issue on GitHub
- Check Streamlit documentation

---

**Enjoy your mobile weather prediction app!** 🌤️📱

Made with ❤️ for mobile-first experience
