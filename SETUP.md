# 🛠️ Setup Guide

Complete setup instructions for the Weather Prediction App.

## Step-by-Step Setup

### 1️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or use the automated script:

```bash
chmod +x run.sh
./run.sh
```

### 2️⃣ Get OpenWeatherMap API Key (Required)

1. Visit [https://openweathermap.org/api](https://openweathermap.org/api)
2. Click "Sign Up" in the top right
3. Create a free account
4. Verify your email
5. Go to [API Keys](https://home.openweathermap.org/api_keys)
6. Copy your default API key (or create a new one)
7. Add to `.env` file:
   ```
   WEATHER_API_KEY=your_api_key_here
   ```

**Note**: Free tier includes:
- 1,000 API calls/day
- Current weather data
- 5-day forecast
- No credit card required

### 3️⃣ Setup Supabase (Optional)

Only needed if you want to persist weather data.

#### Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign in with GitHub
4. Click "New Project"
5. Fill in:
   - Name: "weather-predictions"
   - Database Password: (create a strong password)
   - Region: (choose closest to you)
6. Click "Create new project"
7. Wait 2-3 minutes for setup

#### Get API Credentials

1. Click on "Settings" (gear icon)
2. Go to "API" section
3. Copy two values:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon/public key**: `eyJxxxx...`
4. Add to `.env` file:
   ```
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=eyJxxxx...
   ```

#### Create Database Tables

1. In Supabase dashboard, click "SQL Editor"
2. Click "New Query"
3. Copy and paste this SQL:

```sql
-- Weather observations table
CREATE TABLE weather_observations (
    id BIGSERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(10),
    temperature DECIMAL(5,2),
    feels_like DECIMAL(5,2),
    humidity INTEGER,
    pressure INTEGER,
    wind_speed DECIMAL(5,2),
    condition VARCHAR(50),
    description VARCHAR(200),
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Weather predictions table
CREATE TABLE weather_predictions (
    id BIGSERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(10),
    days_ahead INTEGER,
    predicted_temp DECIMAL(5,2),
    predicted_condition VARCHAR(50),
    temp_state VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_observations_city ON weather_observations(city, country);
CREATE INDEX idx_observations_timestamp ON weather_observations(timestamp);
CREATE INDEX idx_predictions_city ON weather_predictions(city, country);
CREATE INDEX idx_predictions_created ON weather_predictions(created_at);
```

4. Click "RUN"
5. Verify tables created: Go to "Table Editor" and see both tables

### 4️⃣ Configure Environment

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your values:
   ```bash
   nano .env  # or use any text editor
   ```

3. Required configuration:
   ```env
   WEATHER_API_KEY=your_openweathermap_key_here
   ```

4. Optional configuration:
   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your_supabase_anon_key
   DEFAULT_CITY=London
   DEFAULT_COUNTRY=UK
   ```

### 5️⃣ Run the Application

```bash
streamlit run app.py
```

Or use the script:

```bash
./run.sh
```

The app will open at: `http://localhost:8501`

## Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "API Key Invalid"
- Check your OpenWeatherMap API key is correct
- Wait 10-15 minutes after creating a new key (activation time)
- Verify key in `.env` file has no quotes or spaces

### "Database Connection Failed"
- Supabase is optional - app works without it
- Check SUPABASE_URL and SUPABASE_KEY in `.env`
- Verify Supabase project is running

### "No Weather Data"
- Check internet connection
- Verify API key is activated
- Try a different city name
- Check API quota (1000 calls/day free tier)

## Verification

After setup, verify everything works:

1. ✅ App starts without errors
2. ✅ Sidebar shows:
   - Weather API: ✅
   - Database: ✅ (if configured) or ❌ (if skipped)
3. ✅ Can fetch current weather
4. ✅ Can generate predictions

## Next Steps

1. Explore the **Current Weather** tab
2. Generate predictions in **Predictions** tab
3. View analytics in **Analytics** tab
4. Customize settings in sidebar

## Need Help?

- Check the main [README.md](README.md)
- Review error messages in the app
- Check Streamlit logs in terminal
- Verify `.env` file configuration

## Free Tier Limits

### OpenWeatherMap (Free)
- 1,000 calls/day
- 60 calls/minute
- Current weather ✅
- 5-day forecast ✅
- Historical data ❌ (paid only)

### Supabase (Free)
- 500 MB database
- Unlimited API requests
- 2 GB bandwidth/month
- 50 MB file storage

Both are more than enough for personal use!
