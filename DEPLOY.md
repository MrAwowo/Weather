# Streamlit Cloud Deployment Guide

## Step-by-Step Deployment to Streamlit Cloud

### 1️⃣ Verify Repository on GitHub

First, verify your repository exists and is accessible:

**Visit:** https://github.com/MrAwowo/Weather

**Check:**
- ✅ Repository exists
- ✅ Branch `claude/weather-prediction-app-LVHrB` is visible
- ✅ All files are present (app.py, requirements.txt, etc.)

**If repository is private:**
You'll need to make it public OR authorize Streamlit to access private repos (see below).

---

### 2️⃣ Deploy to Streamlit Cloud

**Option A: If Repository is Public**

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click **"Sign in with GitHub"** (important - don't use email!)
3. Authorize Streamlit to access your GitHub account
4. Click **"New app"**
5. Fill in the form:
   - **Repository:** `MrAwowo/Weather`
   - **Branch:** `claude/weather-prediction-app-LVHrB`
   - **Main file path:** `app.py`
6. Click **"Deploy!"**

**Option B: If Repository is Private**

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with GitHub
3. When authorizing, make sure to grant access to private repositories
4. If you don't see your repo:
   - Go to [GitHub Apps Settings](https://github.com/settings/installations)
   - Find "Streamlit Community Cloud"
   - Click "Configure"
   - Under "Repository access":
     - Select "All repositories" OR
     - Select "Only select repositories" and add `MrAwowo/Weather`
   - Click "Save"
5. Go back to Streamlit Cloud and click "New app"
6. You should now see your private repo
7. Fill in:
   - **Repository:** `MrAwowo/Weather`
   - **Branch:** `claude/weather-prediction-app-LVHrB`
   - **Main file path:** `app.py`
8. Click "Deploy!"

---

### 3️⃣ Advanced Settings (Optional)

If you're using Supabase, add environment variables:

1. Before clicking "Deploy", click **"Advanced settings"**
2. Add environment variables:
   ```
   SUPABASE_URL = your_supabase_url
   SUPABASE_KEY = your_supabase_key
   DEFAULT_CITY = London
   DEFAULT_COUNTRY = UK
   ```
3. Click "Save"
4. Click "Deploy!"

**Note:** These are optional! The app works without them.

---

### 4️⃣ Wait for Deployment

- Initial deployment takes 2-5 minutes
- You'll see a build log
- Once complete, you'll get a URL like: `https://your-app-name.streamlit.app`

---

### 5️⃣ Access on Your Phone

1. Open the Streamlit URL on your phone
2. Install as PWA:
   - **iPhone:** Safari → Share → "Add to Home Screen"
   - **Android:** Chrome → Menu → "Add to Home Screen"
3. Done! 🎉

---

## 🐛 Troubleshooting

### "Repository not found"

**Solution 1: Make Repository Public**
```
GitHub → Settings → Change visibility → Make public
```

**Solution 2: Grant Access to Private Repo**
```
GitHub → Settings → Applications → Streamlit Community Cloud → Configure
→ Repository access → Select your repo → Save
```

### "Branch not found"

Make sure you select the correct branch:
- Branch name: `claude/weather-prediction-app-LVHrB`
- NOT `main` or `master`

### "Build failed"

Check the logs. Common issues:
- Missing `requirements.txt` (we have this ✅)
- Wrong `app.py` path (should be just `app.py` ✅)
- Python version mismatch (add `.python-version` file if needed)

---

## 🚀 Alternative: Railway (If Streamlit Doesn't Work)

Railway is even easier and supports private repos automatically:

1. Go to **[railway.app](https://railway.app)**
2. Sign in with GitHub
3. Click "New Project"
4. Click "Deploy from GitHub repo"
5. Select `MrAwowo/Weather`
6. Railway auto-detects Streamlit
7. Click "Deploy"
8. Get your URL: `https://your-app.up.railway.app`

**Advantage:** Works with private repos by default, no extra setup needed.

---

## 📋 Quick Checklist

Before deploying, verify:

- [ ] Repository exists on GitHub
- [ ] Branch `claude/weather-prediction-app-LVHrB` is pushed
- [ ] Files are present: `app.py`, `requirements.txt`, `.streamlit/config.toml`
- [ ] Repository is public OR you've granted access
- [ ] You're signing in with GitHub (not email)

---

## 💡 Recommended: Make Repository Public

**Why make it public?**
- ✅ Easiest deployment
- ✅ No access configuration needed
- ✅ Can share with friends
- ✅ Good for portfolio
- ✅ No secrets in the code

**Your repo contains:**
- Python code (safe to share)
- No API keys (using Open-Meteo)
- No passwords
- No sensitive data

**To make public:**
```
1. Go to: https://github.com/MrAwowo/Weather
2. Settings → Danger Zone → Change visibility
3. Make public → Confirm
```

---

## ✅ After Deployment

Once deployed, you'll have:
- Public URL (e.g., `https://weather-predict.streamlit.app`)
- Auto-updates when you push to GitHub
- Free hosting
- HTTPS (required for PWA)
- Analytics dashboard

**Then install on your phone as PWA!** 📱

---

Need help? Let me know which step you're stuck on!
