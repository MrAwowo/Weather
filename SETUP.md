# 🛠️ Setup Guide

Complete setup instructions for the Weather Prediction App.

## 🎉 Great News: No API Key Required!

This app uses **Open-Meteo**, a truly public weather API. You can start using it immediately without any API keys or registration!

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

### 2️⃣ Run the App

```bash
streamlit run app.py
```

**That's it!** The app will open at `http://localhost:8501` 🚀

No configuration files needed. No API keys. Just install and run!

---

## 🔧 Optional: Supabase Setup

Only needed if you want to persist weather data and predictions.

### Create Supabase Project

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

### Get API Credentials

1. Click on "Settings" (gear icon)
2. Go to "API" section
3. Copy two values:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon/public key**: `eyJxxxx...`
4. Create `.env` file in the project root:
   ```env
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=eyJxxxx...
   DEFAULT_CITY=London
   DEFAULT_COUNTRY=UK
   ```

### Create Database Tables

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

---

## 🌍 About Open-Meteo

**Open-Meteo** is the weather data source for this app. It's completely free and open:

### What You Get:
- ✅ **Current Weather**: Real-time conditions worldwide
- ✅ **Forecasts**: Up to 16 days ahead
- ✅ **Historical Data**: Weather archives going back decades
- ✅ **No Authentication**: Zero API keys needed
- ✅ **No Rate Limits**: Unlimited requests for non-commercial use
- ✅ **High Quality**: Data from national weather services

### Why It's Better:
- **Accessibility**: Anyone can use it immediately
- **Privacy**: No tracking, no accounts, no data collection
- **Reliability**: Backed by official weather services
- **Community**: Open-source and transparent
- **Global**: Works for any location worldwide

Learn more: [open-meteo.com](https://open-meteo.com/)

---

## 📝 Configuration (Optional)

You can optionally create a `.env` file to customize default settings:

```env
# Default location (optional)
DEFAULT_CITY=London
DEFAULT_COUNTRY=UK

# Supabase (optional - only if you want data persistence)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

**Note:** All settings are optional! The app works perfectly without any `.env` file.

---

## 🐛 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Could not find location"
- Check your internet connection
- Try using a major city name (e.g., "London", "New York")
- Verify spelling and try without country code
- The geocoding uses OpenStreetMap Nominatim

### "No historical data"
- Check internet connection
- Verify the date range (Open-Meteo has data from 1940 onwards)
- Try a different location

### "Database Connection Failed"
- Supabase is optional - app works without it
- Check SUPABASE_URL and SUPABASE_KEY in `.env`
- Verify Supabase project is running
- Ensure database tables are created

### Geocoding Too Slow
- First lookup may be slow due to geocoding
- Subsequent requests for the same city are faster
- Consider adding manual coordinates in the code if needed

---

## ✅ Verification

After setup, verify everything works:

1. ✅ App starts without errors
2. ✅ Sidebar shows:
   - Weather API: ✅ (Open-Meteo - Public)
   - Database: ✅ (if configured) or ❌ (Optional) (if skipped)
3. ✅ Can fetch current weather
4. ✅ Can generate predictions
5. ✅ Predictions use REAL historical data

---

## 🚀 Next Steps

1. Explore the **Current Weather** tab
2. Generate predictions in **Predictions** tab
3. View analytics in **Analytics** tab
4. Customize settings in sidebar
5. Try different cities worldwide
6. Experiment with different Markov chain orders
7. Adjust historical data range to see how it affects predictions

---

## 💡 Tips

- **Historical Data**: More data (90-365 days) = better Markov chain training
- **Markov Order**: Order 2 balances accuracy and complexity
- **Prediction Days**: Start with 7 days for reasonable accuracy
- **City Names**: Use English names (e.g., "Munich" not "München")
- **Country Codes**: Use 2-letter ISO codes (US, UK, DE, FR, etc.)

---

## 🔬 Advanced Usage

### Custom Temperature States

Edit `markov_predictor.py` to customize temperature ranges:

```python
def _discretize_temperature(self, temp):
    if temp < 0:
        return "freezing"
    elif temp < 10:
        return "cold"
    # Add your custom ranges here
```

### Adjust Prediction Algorithm

Modify the Markov chain order in `config.py`:

```python
MARKOV_ORDER = 3  # Try third-order for more context
```

### Add More Weather Variables

Extend the model to include:
- Precipitation
- Wind direction
- Cloud cover
- Pressure systems

---

## 📊 Data Quality

**Open-Meteo Data Sources:**
- NOAA (US)
- DWD (Germany)
- Météo-France (France)
- And many other national weather services

**Quality Assurance:**
- Professional weather stations
- Satellite data integration
- Quality-controlled archives
- Regular updates

---

## 🆘 Need Help?

- Check the main [README.md](README.md)
- Review error messages in the app
- Check Streamlit logs in terminal
- Visit [Open-Meteo Documentation](https://open-meteo.com/en/docs)
- Open an issue on GitHub

---

## 🎓 Educational Use

This app is perfect for:
- Learning Markov chains
- Understanding weather patterns
- Teaching probability and statistics
- Demonstrating API integration
- Exploring time series prediction

**No barriers to entry** - students can run it immediately without setting up accounts or managing API keys!

---

## 🌟 What Makes This Special

Unlike other weather apps that require API keys:

1. **Zero Friction**: Install and run, no configuration
2. **Real Data**: Actual historical weather, not simulated
3. **Educational**: Perfect for teaching and learning
4. **Privacy**: No tracking or data collection
5. **Free Forever**: No hidden costs or limitations

---

Made with ❤️ using Open-Meteo and Python

**Start predicting weather in 30 seconds!** 🌤️
