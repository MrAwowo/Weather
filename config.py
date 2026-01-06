import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Weather API Configuration
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WEATHER_API_BASE_URL = "https://api.openweathermap.org/data/2.5"

# Default Settings
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "London")
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "UK")

# Markov Chain Configuration
MARKOV_ORDER = 2  # Second-order Markov chain
PREDICTION_DAYS = 7  # Number of days to predict
