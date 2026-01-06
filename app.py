import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from weather_api import WeatherAPI
from markov_predictor import WeatherMarkovChain
from database import WeatherDatabase
import config

# Page configuration
st.set_page_config(
    page_title="Weather Prediction",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://github.com/yourusername/Weather',
        'Report a bug': 'https://github.com/yourusername/Weather/issues',
        'About': '# Weather Prediction App\nPowered by Open-Meteo & Markov Chains'
    }
)

# Mobile-responsive CSS
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
<meta name="theme-color" content="#2193b0">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Weather Predict">
<link rel="manifest" href="/manifest.json">
<style>
    /* Base styles */
    :root {
        --primary-blue: #2193b0;
        --primary-light: #6dd5ed;
        --purple: #667eea;
        --purple-dark: #764ba2;
        --pink: #f093fb;
        --red: #f5576c;
    }

    /* Mobile-first responsive header */
    .main-header {
        font-size: clamp(1.5rem, 5vw, 3rem);
        font-weight: bold;
        background: linear-gradient(120deg, var(--primary-blue), var(--primary-light));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 0.5rem 0;
        margin-bottom: 1rem;
    }

    /* Touch-friendly buttons */
    .stButton>button {
        background: linear-gradient(120deg, var(--primary-blue), var(--primary-light));
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1rem;
        min-height: 44px; /* iOS minimum touch target */
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background: linear-gradient(120deg, #1a7a93, #5ac4dc);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(33, 147, 176, 0.4);
    }

    .stButton>button:active {
        transform: translateY(0);
    }

    /* Mobile-optimized cards */
    .metric-card {
        background: linear-gradient(135deg, var(--purple) 0%, var(--purple-dark) 100%);
        padding: 1rem;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
    }

    .prediction-card {
        background: linear-gradient(135deg, var(--pink) 0%, var(--red) 100%);
        padding: 0.75rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
        text-align: center;
    }

    /* Info boxes */
    .info-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid var(--primary-blue);
        margin: 0.5rem 0;
    }

    /* Mobile sidebar optimization */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.75rem;
            padding: 0.5rem 0;
        }

        /* Larger touch targets on mobile */
        .stButton>button {
            padding: 1rem 1.5rem;
            font-size: 1.1rem;
        }

        /* Optimize metric display */
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.05);
            padding: 0.75rem;
            border-radius: 8px;
            margin: 0.25rem 0;
        }

        /* Stack columns on mobile */
        [data-testid="column"] {
            padding: 0.25rem !important;
        }

        /* Improve tab navigation */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            flex-wrap: wrap;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem 0.75rem;
            font-size: 0.9rem;
        }
    }

    /* Tablet optimization */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main-header {
            font-size: 2.5rem;
        }
    }

    /* Desktop optimization */
    @media (min-width: 1025px) {
        .main-header {
            font-size: 3rem;
        }
    }

    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .info-box {
            background: rgba(240, 242, 246, 0.1);
        }
    }

    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }

    /* Loading states */
    .stSpinner > div {
        border-top-color: var(--primary-blue) !important;
    }

    /* Improve input fields on mobile */
    input, select, textarea {
        font-size: 16px !important; /* Prevents zoom on iOS */
    }

    /* Weather icon sizing */
    .weather-icon {
        font-size: clamp(3rem, 10vw, 5rem);
    }

    /* Prediction cards grid */
    .prediction-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 0.75rem;
        margin: 1rem 0;
    }

    /* PWA install banner */
    .install-banner {
        background: linear-gradient(120deg, var(--primary-blue), var(--primary-light));
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'weather_api' not in st.session_state:
    st.session_state.weather_api = WeatherAPI()
if 'database' not in st.session_state:
    st.session_state.database = WeatherDatabase()
if 'markov_model' not in st.session_state:
    st.session_state.markov_model = WeatherMarkovChain(order=config.MARKOV_ORDER)
if 'predictions' not in st.session_state:
    st.session_state.predictions = None
if 'current_weather' not in st.session_state:
    st.session_state.current_weather = None

def get_weather_icon(condition):
    """Return emoji icon for weather condition"""
    icons = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "🌨️",
        "Mist": "🌫️",
        "Fog": "🌫️"
    }
    return icons.get(condition, "🌤️")

def main():
    # Header
    st.markdown('<h1 class="main-header">🌤️ Weather Prediction with Markov Chains</h1>', unsafe_allow_html=True)

    # Mobile install banner
    if 'hide_install_banner' not in st.session_state:
        st.session_state.hide_install_banner = False

    if not st.session_state.hide_install_banner:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.info("📱 **Mobile App:** Install this on your phone! See [MOBILE_INSTALL.md](MOBILE_INSTALL.md) for instructions.")
        with col2:
            if st.button("✕", key="close_banner"):
                st.session_state.hide_install_banner = True
                st.rerun()

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        city = st.text_input("City", value=config.DEFAULT_CITY,
                            help="Type any city name (e.g., Paris, Tokyo, New York)")
        country = st.text_input("Country Code (optional)", value=config.DEFAULT_COUNTRY, max_chars=2,
                               help="2-letter code like US, UK, FR (optional)")

        st.divider()

        st.subheader("🔮 Prediction Settings")
        prediction_days = st.slider("Days to Predict", 1, 14, config.PREDICTION_DAYS)
        markov_order = st.selectbox("Markov Chain Order", [1, 2, 3], index=1)

        st.divider()

        st.subheader("📊 Data Settings")
        historical_days = st.slider("Historical Data (days)", 30, 365, 180,
                                   help="More days = better predictions (requires internet)")

        st.divider()

        # API Status
        st.subheader("🔌 Status")
        db_configured = st.session_state.database.enabled

        st.write(f"Weather API: ✅ (Open-Meteo - Public)")
        st.write(f"Database: {'✅' if db_configured else '❌ (Optional)'}")

        st.divider()

        # About
        with st.expander("ℹ️ About"):
            st.write("""
            This app uses **Markov Chains** to predict future weather patterns based on historical data.

            **How it works:**
            1. Fetches current weather data
            2. Gets REAL historical weather data
            3. Trains a Markov chain model
            4. Generates probabilistic predictions

            **Tech Stack:**
            - Streamlit for UI
            - Open-Meteo API (truly public, no key!)
            - Supabase for data storage (optional)
            - Python for ML
            """)

    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Current Weather", "🔮 Predictions", "📊 Analytics", "⚙️ Setup"])

    with tab1:
        st.header(f"Current Weather in {city}, {country}")

        col1, col2 = st.columns([2, 1])

        with col1:
            if st.button("🔄 Fetch Current Weather", use_container_width=True):
                with st.spinner("Fetching weather data..."):
                    data = st.session_state.weather_api.get_current_weather(city, country)
                    parsed = st.session_state.weather_api.parse_current_weather(data)

                    if parsed:
                        st.session_state.current_weather = parsed

                        # Save to database
                        if st.session_state.database.enabled:
                            st.session_state.database.save_weather_observation(
                                city, country, parsed
                            )

        if st.session_state.current_weather:
            weather = st.session_state.current_weather

            # Display current weather
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("🌡️ Temperature", f"{weather['temp']:.1f}°C",
                         f"Feels like {weather['feels_like']:.1f}°C")

            with col2:
                st.metric("💧 Humidity", f"{weather['humidity']}%")

            with col3:
                st.metric("💨 Wind Speed", f"{weather['wind_speed']} m/s")

            with col4:
                st.metric("🔽 Pressure", f"{weather['pressure']} hPa")

            st.divider()

            # Weather condition
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"<div style='font-size: 5rem; text-align: center;'>{get_weather_icon(weather['condition'])}</div>",
                           unsafe_allow_html=True)
            with col2:
                st.markdown(f"### {weather['condition']}")
                st.markdown(f"*{weather['description'].capitalize()}*")
                st.markdown(f"**Min/Max:** {weather['temp_min']:.1f}°C / {weather['temp_max']:.1f}°C")

    with tab2:
        st.header("🔮 Weather Predictions")

        if st.button("🚀 Generate Predictions", use_container_width=True):
            with st.spinner("Training Markov Chain and generating predictions..."):
                try:
                    # Show progress
                    progress_text = st.empty()
                    progress_text.info(f"🔍 Finding location: {city}...")

                    # Get historical data from Open-Meteo (real data!)
                    end_date = datetime.now().strftime("%Y-%m-%d")
                    start_date = (datetime.now() - timedelta(days=historical_days)).strftime("%Y-%m-%d")

                    progress_text.info(f"📥 Fetching {historical_days} days of weather history...")
                    historical = st.session_state.weather_api.get_historical_data(city, country, start_date, end_date)
                    progress_text.empty()

                    if not historical or len(historical) == 0:
                        st.error(f"❌ Could not fetch historical data for {city}. Please check:\n"
                               f"- City name is spelled correctly\n"
                               f"- Internet connection is working\n"
                               f"- Try a major city name")
                        st.stop()

                    if len(historical) < markov_order + 1:
                        st.error(f"❌ Not enough historical data to train model.\n"
                               f"- Got {len(historical)} days of data\n"
                               f"- Need at least {markov_order + 1} days\n"
                               f"- Try increasing the 'Historical Data' slider")
                        st.stop()

                    if len(historical) > markov_order:
                        # Train model
                        model = WeatherMarkovChain(order=markov_order)
                        model.train(historical)
                        st.session_state.markov_model = model

                        # Generate predictions
                        recent_data = historical[-markov_order-5:]
                        predictions = model.predict(recent_data, days=prediction_days)
                        st.session_state.predictions = predictions

                        # Save to database
                        if st.session_state.database.enabled:
                            st.session_state.database.save_prediction(city, country, predictions)

                        st.success(f"✅ Generated {prediction_days}-day predictions using {len(historical)} days of historical data!")
                    else:
                        st.error(f"❌ Not enough historical data. Got {len(historical)} days, need at least {markov_order + 1}")

                except Exception as e:
                    st.error(f"Error generating predictions: {str(e)}")

        # Display predictions
        if st.session_state.predictions:
            predictions = st.session_state.predictions

            # Create prediction dataframe
            pred_dates = [(datetime.now() + timedelta(days=i+1)).strftime("%Y-%m-%d")
                         for i in range(len(predictions))]

            pred_df = pd.DataFrame({
                "Date": pred_dates,
                "Temperature (°C)": [p['temp'] for p in predictions],
                "Condition": [p['condition'] for p in predictions],
                "State": [p['temp_state'] for p in predictions]
            })

            # Temperature prediction chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=pred_df['Date'],
                y=pred_df['Temperature (°C)'],
                mode='lines+markers',
                name='Predicted Temperature',
                line=dict(color='#f5576c', width=3),
                marker=dict(size=10)
            ))

            fig.update_layout(
                title="Temperature Prediction",
                xaxis_title="Date",
                yaxis_title="Temperature (°C)",
                hovermode='x unified',
                template='plotly_white',
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

            # Prediction cards
            st.subheader("Daily Predictions")

            cols = st.columns(min(len(predictions), 7))
            for i, (col, pred, date) in enumerate(zip(cols, predictions, pred_dates)):
                with col:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                padding: 1rem; border-radius: 10px; color: white; text-align: center;'>
                        <div style='font-size: 0.8rem; opacity: 0.9;'>{date}</div>
                        <div style='font-size: 2rem;'>{get_weather_icon(pred['condition'])}</div>
                        <div style='font-size: 1.5rem; font-weight: bold;'>{pred['temp']:.1f}°C</div>
                        <div style='font-size: 0.9rem;'>{pred['condition']}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Full prediction table
            st.divider()
            st.subheader("Detailed Predictions")
            st.dataframe(pred_df, use_container_width=True, hide_index=True)

    with tab3:
        st.header("📊 Analytics & Insights")

        if st.session_state.predictions and st.session_state.markov_model.trained:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Temperature Distribution")

                # Temperature state distribution
                temp_states = [p['temp_state'] for p in st.session_state.predictions]
                temp_df = pd.DataFrame({'State': temp_states})
                state_counts = temp_df['State'].value_counts()

                fig = px.pie(values=state_counts.values, names=state_counts.index,
                           title="Predicted Temperature States",
                           color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("Weather Conditions")

                # Condition distribution
                conditions = [p['condition'] for p in st.session_state.predictions]
                cond_df = pd.DataFrame({'Condition': conditions})
                cond_counts = cond_df['Condition'].value_counts()

                fig = px.bar(x=cond_counts.index, y=cond_counts.values,
                           labels={'x': 'Condition', 'y': 'Count'},
                           title="Predicted Weather Conditions",
                           color=cond_counts.values,
                           color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)

            # Transition probabilities
            st.divider()
            st.subheader("🔄 Markov Chain Transition Probabilities")

            trans_probs = st.session_state.markov_model.get_transition_probabilities("temp")

            if trans_probs:
                st.write("**Temperature State Transitions** (showing most common transitions)")

                # Convert to dataframe for display
                trans_data = []
                for current, next_states in list(trans_probs.items())[:10]:
                    for next_state, prob in next_states.items():
                        trans_data.append({
                            "Current State": " → ".join(current),
                            "Next State": next_state,
                            "Probability": f"{prob:.2%}"
                        })

                if trans_data:
                    trans_df = pd.DataFrame(trans_data)
                    st.dataframe(trans_df, use_container_width=True, hide_index=True)

        else:
            st.info("👆 Generate predictions first to see analytics")

    with tab4:
        st.header("⚙️ Setup Instructions")

        st.markdown("""
        ### 🚀 Quick Start

        **No API Key Required!** This app uses [Open-Meteo](https://open-meteo.com/),
        a truly public weather API. Just run the app!

        ```bash
        pip install -r requirements.txt
        streamlit run app.py
        ```

        **Optional:** Setup Supabase for data persistence
        - Create account at [Supabase](https://supabase.com)
        - Create a new project
        - Copy URL and anon key to `.env` file
        - Run the SQL below in Supabase SQL Editor
        """)

        st.divider()

        st.subheader("📋 Database Schema")

        sql = st.session_state.database.create_tables_sql()

        st.code(sql, language="sql")

        if st.button("📋 Copy SQL to Clipboard"):
            st.toast("SQL copied! (Paste in Supabase SQL Editor)")

        st.divider()

        st.subheader("📄 Environment Variables")

        st.code("""
# .env file (all optional!)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
DEFAULT_CITY=London
DEFAULT_COUNTRY=UK

# No WEATHER_API_KEY needed - using Open-Meteo!
        """, language="bash")

        st.divider()

        st.subheader("💻 Installation")

        st.code("""
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
        """, language="bash")

if __name__ == "__main__":
    main()
