# 🌤️ Weather Prediction with Markov Chains

A modern, interactive weather prediction application that uses Markov Chains to forecast weather patterns. Built with Streamlit, Python, and **Open-Meteo** (truly public weather API - **no API key required!**).

![Weather Prediction App](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red.svg)
![Open--Meteo](https://img.shields.io/badge/Weather-Open--Meteo-green.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- 📱 **Mobile PWA** - Install as an app on your phone! Works offline!
- 🌡️ **Real-time Weather Data** - Fetch current weather from Open-Meteo (no API key!)
- 📜 **REAL Historical Data** - Access actual historical weather patterns (not simulated!)
- 🔮 **Markov Chain Predictions** - Probabilistic weather forecasting using historical patterns
- 📊 **Interactive Visualizations** - Beautiful charts powered by Plotly
- 💾 **Data Persistence** - Optional Supabase integration for storing observations and predictions
- 🎨 **Modern UI** - Mobile-first responsive design with smooth animations
- ⚙️ **Configurable** - Adjust prediction days, Markov chain order, and historical data range
- 🆓 **100% Free** - No API keys, no registration, no limits!

## 🏗️ Architecture

### How It Works

1. **Data Collection**: Fetches current weather data from Open-Meteo API
2. **Historical Data**: Retrieves REAL historical weather patterns from Open-Meteo Archive (90-365 days)
3. **Model Training**: Trains a Markov Chain model on temperature states and weather conditions
4. **Prediction**: Generates probabilistic forecasts for 1-14 days ahead
5. **Visualization**: Displays predictions with interactive charts and metrics

### Why Open-Meteo?

**Open-Meteo** is a truly public weather API:
- ✅ **No API Key Required** - Zero authentication needed
- ✅ **No Registration** - Start using immediately
- ✅ **Unlimited Requests** - No rate limits for non-commercial use
- ✅ **Historical Data Included** - Free access to weather archives
- ✅ **Global Coverage** - Weather data worldwide
- ✅ **Open Source** - Community-driven and transparent
- ✅ **Perfect for Learning** - Anyone can run this app instantly!

Learn more: [open-meteo.com](https://open-meteo.com/)

### Markov Chain Model

The app uses a **second-order Markov chain** by default, meaning it considers the previous 2 days to predict the next day's weather. This captures short-term weather patterns and dependencies.

**Temperature States:**
- Freezing: < 0°C
- Cold: 0-10°C
- Mild: 10-20°C
- Warm: 20-30°C
- Hot: > 30°C

**Weather Conditions:**
- Clear, Clouds, Rain, Drizzle, Thunderstorm, Snow, Fog

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- **No API keys needed!** 🎉
- Supabase account (optional, for data persistence)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Weather
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`

That's it! No configuration needed. Start predicting weather immediately! 🚀

## 📱 Mobile Installation

**Install as a mobile app on your phone!**

This is a Progressive Web App (PWA) - it can be installed on your phone's home screen and works like a native app.

### Quick Install:

**iPhone:**
1. Open in Safari
2. Tap Share → "Add to Home Screen"

**Android:**
1. Open in Chrome
2. Tap Menu → "Add to Home Screen"

**Full instructions:** See [MOBILE_INSTALL.md](MOBILE_INSTALL.md) for detailed deployment and installation guides.

### PWA Features:
- ✅ Works offline (with cached data)
- ✅ Full-screen experience
- ✅ Home screen icon
- ✅ Push notifications (future)
- ✅ Auto-updates

## ⚙️ Optional: Supabase Setup

If you want to persist weather data and predictions, set up Supabase:

1. Go to [Supabase](https://supabase.com)
2. Create a new account and project
3. Go to Project Settings → API
4. Copy the Project URL and anon/public key
5. Create `.env` file:
   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your_supabase_anon_key
   DEFAULT_CITY=London
   DEFAULT_COUNTRY=UK
   ```
6. Run the SQL schema (available in the app's Setup tab)

## 🗄️ Database Setup (Optional)

If you want to persist weather data and predictions, set up Supabase:

1. Create a Supabase project
2. Go to SQL Editor
3. Run the following schema:

```sql
-- Table for weather observations
CREATE TABLE IF NOT EXISTS weather_observations (
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

-- Table for weather predictions
CREATE TABLE IF NOT EXISTS weather_predictions (
    id BIGSERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(10),
    days_ahead INTEGER,
    predicted_temp DECIMAL(5,2),
    predicted_condition VARCHAR(50),
    temp_state VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_observations_city ON weather_observations(city, country);
CREATE INDEX idx_observations_timestamp ON weather_observations(timestamp);
CREATE INDEX idx_predictions_city ON weather_predictions(city, country);
CREATE INDEX idx_predictions_created ON weather_predictions(created_at);
```

## 📖 Usage

### Current Weather Tab
- Enter a city and country code
- Click "Fetch Current Weather"
- View current temperature, humidity, wind speed, and conditions

### Predictions Tab
- Configure prediction settings in the sidebar
- Click "Generate Predictions"
- View temperature forecasts for up to 14 days
- See daily prediction cards with weather icons

### Analytics Tab
- View temperature state distribution
- Analyze weather condition frequencies
- Examine Markov chain transition probabilities

### Setup Tab
- Follow step-by-step setup instructions
- Copy database schema SQL
- View environment variable examples

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.9+
- **ML Model**: Custom Markov Chain implementation
- **Data Visualization**: Plotly
- **Weather API**: Open-Meteo (public, no key required!)
- **Geocoding**: Geopy (OpenStreetMap Nominatim)
- **Database**: Supabase (PostgreSQL) - Optional
- **Additional Libraries**: pandas, numpy, scipy

## ⚙️ Configuration

Edit `config.py` to customize:

```python
MARKOV_ORDER = 2          # Chain order (1-3)
PREDICTION_DAYS = 7       # Default prediction days
DEFAULT_CITY = "London"   # Default city
DEFAULT_COUNTRY = "UK"    # Default country code
```

## 📁 Project Structure

```
Weather/
├── app.py                  # Main Streamlit application (mobile-optimized!)
├── weather_api.py          # Open-Meteo API client
├── markov_predictor.py     # Markov Chain model
├── database.py             # Supabase database handler
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── .streamlit/            # Streamlit & PWA configuration
│   ├── config.toml        # App settings (mobile-optimized)
│   └── manifest.json      # PWA manifest
├── README.md              # This file
├── SETUP.md               # Detailed setup guide
├── MOBILE_INSTALL.md      # Mobile installation & deployment guide
└── run.sh                 # Automated startup script
```

## 🎨 Features Walkthrough

### Markov Chain Predictions
The app uses probabilistic modeling to predict weather:
- Trains on REAL historical weather data
- Considers temperature states and conditions
- Generates multi-day forecasts
- Shows transition probabilities

### Interactive Visualizations
- Line charts for temperature trends
- Pie charts for state distributions
- Bar charts for condition frequencies
- Daily prediction cards with icons

### Data Persistence (Optional)
- Stores weather observations
- Saves prediction history
- Enables historical analysis
- Tracks model accuracy over time

## 🌍 Data Sources

This application uses **Open-Meteo**, a free and open-source weather API:

- **Current Weather**: [Open-Meteo Forecast API](https://open-meteo.com/en/docs)
- **Historical Data**: [Open-Meteo Archive](https://open-meteo.com/en/docs/historical-weather-api)
- **Geocoding**: OpenStreetMap Nominatim (via Geopy)

All data sources are completely free with no API keys required!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Open-Meteo](https://open-meteo.com) for providing truly free, public weather data
- [Streamlit](https://streamlit.io) for the amazing framework
- [Supabase](https://supabase.com) for database infrastructure
- [Plotly](https://plotly.com) for interactive visualizations
- [OpenStreetMap](https://www.openstreetmap.org) for geocoding services

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review the Setup tab in the app

## 🚀 Future Enhancements

- [ ] Machine learning models (LSTM, Prophet)
- [ ] Multiple location comparison
- [ ] Historical accuracy metrics
- [ ] Weather alerts and notifications
- [ ] Export predictions to CSV/PDF
- [ ] Mobile responsive design improvements
- [ ] Multi-language support
- [ ] Ensemble predictions combining multiple models

## 🎯 Why This Project?

This project demonstrates:
- ✅ **Accessible ML**: No barriers to entry - works out of the box
- ✅ **Real Data**: Uses actual historical weather data
- ✅ **Privacy-First**: No API keys = no tracking
- ✅ **Mobile-First**: PWA works on any device, install as app
- ✅ **Educational**: Perfect for learning Markov chains and weather prediction
- ✅ **Production-Ready**: Clean code, good architecture, scalable design

---

Made with ❤️ using Streamlit, Python, and Open-Meteo

**No API keys. No limits. Just weather predictions.** 🌤️
