import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase Configuration (Optional - for data persistence)
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Weather API Configuration
# Using Open-Meteo - NO API KEY REQUIRED!
# Open-Meteo is a free, open-source weather API
# Learn more: https://open-meteo.com/

# Default Settings
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "London")
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "UK")

# Markov Chain Configuration
MARKOV_ORDER = 2  # Second-order Markov chain
PREDICTION_DAYS = 7  # Number of days to predict
