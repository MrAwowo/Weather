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
    page_title="Weather Prediction with Markov Chains",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern design
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(120deg, #2193b0, #6dd5ed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .prediction-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
    }
    .info-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2193b0;
    }
    .stButton>button {
        background: linear-gradient(120deg, #2193b0, #6dd5ed);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: linear-gradient(120deg, #1a7a93, #5ac4dc);
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

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        city = st.text_input("City", value=config.DEFAULT_CITY)
        country = st.text_input("Country Code", value=config.DEFAULT_COUNTRY, max_chars=2)

        st.divider()

        st.subheader("🔮 Prediction Settings")
        prediction_days = st.slider("Days to Predict", 1, 14, config.PREDICTION_DAYS)
        markov_order = st.selectbox("Markov Chain Order", [1, 2, 3], index=1)

        st.divider()

        st.subheader("📊 Data Settings")
        historical_days = st.slider("Historical Data (days)", 30, 365, 90)

        st.divider()

        # API Status
        st.subheader("🔌 Status")
        api_configured = bool(config.WEATHER_API_KEY)
        db_configured = st.session_state.database.enabled

        st.write(f"Weather API: {'✅' if api_configured else '❌'}")
        st.write(f"Database: {'✅' if db_configured else '❌'}")

        if not api_configured:
            st.warning("⚠️ Set WEATHER_API_KEY in .env file")

        st.divider()

        # About
        with st.expander("ℹ️ About"):
            st.write("""
            This app uses **Markov Chains** to predict future weather patterns based on historical data.

            **How it works:**
            1. Fetches current weather data
            2. Simulates historical weather patterns
            3. Trains a Markov chain model
            4. Generates probabilistic predictions

            **Tech Stack:**
            - Streamlit for UI
            - OpenWeatherMap API
            - Supabase for data storage
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
                    # Get historical data (simulated for demo)
                    end_date = datetime.now().strftime("%Y-%m-%d")
                    start_date = (datetime.now() - timedelta(days=historical_days)).strftime("%Y-%m-%d")

                    historical = st.session_state.weather_api.get_historical_data(0, 0, start_date, end_date)

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

                        st.success(f"✅ Generated {prediction_days}-day predictions!")
                    else:
                        st.error("Not enough historical data to train model")

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

        1. **Get Weather API Key** (Required)
           - Sign up at [OpenWeatherMap](https://openweathermap.org/api)
           - Get your free API key
           - Add to `.env` file: `WEATHER_API_KEY=your_key_here`

        2. **Setup Supabase** (Optional - for data persistence)
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
# .env file
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
WEATHER_API_KEY=your-openweathermap-key
DEFAULT_CITY=London
DEFAULT_COUNTRY=UK
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
