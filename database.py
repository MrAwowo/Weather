from supabase import create_client, Client
from datetime import datetime
import config

class WeatherDatabase:
    """Handle Supabase database operations for weather data"""

    def __init__(self):
        """Initialize Supabase client"""
        if not config.SUPABASE_URL or not config.SUPABASE_KEY:
            self.client = None
            self.enabled = False
        else:
            try:
                self.client: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
                self.enabled = True
            except Exception as e:
                print(f"Failed to connect to Supabase: {e}")
                self.client = None
                self.enabled = False

    def save_weather_observation(self, city, country, weather_data):
        """Save a weather observation to the database"""
        if not self.enabled:
            return {"error": "Database not configured"}

        try:
            data = {
                "city": city,
                "country": country,
                "temperature": weather_data.get("temp"),
                "feels_like": weather_data.get("feels_like"),
                "humidity": weather_data.get("humidity"),
                "pressure": weather_data.get("pressure"),
                "wind_speed": weather_data.get("wind_speed"),
                "condition": weather_data.get("condition"),
                "description": weather_data.get("description"),
                "timestamp": weather_data.get("timestamp", datetime.now()).isoformat()
            }

            result = self.client.table("weather_observations").insert(data).execute()
            return result
        except Exception as e:
            return {"error": str(e)}

    def save_prediction(self, city, country, predictions):
        """Save weather predictions to the database"""
        if not self.enabled:
            return {"error": "Database not configured"}

        try:
            prediction_records = []
            for i, pred in enumerate(predictions, 1):
                prediction_records.append({
                    "city": city,
                    "country": country,
                    "days_ahead": i,
                    "predicted_temp": pred.get("temp"),
                    "predicted_condition": pred.get("condition"),
                    "temp_state": pred.get("temp_state"),
                    "created_at": datetime.now().isoformat()
                })

            result = self.client.table("weather_predictions").insert(prediction_records).execute()
            return result
        except Exception as e:
            return {"error": str(e)}

    def get_historical_observations(self, city, country, limit=100):
        """Get historical weather observations for a location"""
        if not self.enabled:
            return []

        try:
            result = self.client.table("weather_observations")\
                .select("*")\
                .eq("city", city)\
                .eq("country", country)\
                .order("timestamp", desc=True)\
                .limit(limit)\
                .execute()

            return result.data if result.data else []
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return []

    def get_recent_predictions(self, city, country, limit=10):
        """Get recent predictions for a location"""
        if not self.enabled:
            return []

        try:
            result = self.client.table("weather_predictions")\
                .select("*")\
                .eq("city", city)\
                .eq("country", country)\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()

            return result.data if result.data else []
        except Exception as e:
            print(f"Error fetching predictions: {e}")
            return []

    def create_tables_sql(self):
        """
        Return SQL statements to create necessary tables
        Run these in your Supabase SQL editor
        """
        return """
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

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_observations_city ON weather_observations(city, country);
CREATE INDEX IF NOT EXISTS idx_observations_timestamp ON weather_observations(timestamp);
CREATE INDEX IF NOT EXISTS idx_predictions_city ON weather_predictions(city, country);
CREATE INDEX IF NOT EXISTS idx_predictions_created ON weather_predictions(created_at);
"""
