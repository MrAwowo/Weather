import requests
from datetime import datetime, timedelta
import config

class WeatherAPI:
    """Fetch weather data from OpenWeatherMap API"""

    def __init__(self):
        self.api_key = config.WEATHER_API_KEY
        self.base_url = config.WEATHER_API_BASE_URL

    def get_current_weather(self, city, country_code=""):
        """Get current weather for a city"""
        try:
            location = f"{city},{country_code}" if country_code else city
            url = f"{self.base_url}/weather"
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "metric"
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_forecast(self, city, country_code="", days=5):
        """Get weather forecast for a city (up to 5 days)"""
        try:
            location = f"{city},{country_code}" if country_code else city
            url = f"{self.base_url}/forecast"
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "metric"
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_historical_data(self, lat, lon, start_date, end_date):
        """
        Get historical weather data (Note: This requires a paid API subscription)
        For demo purposes, we'll return simulated data
        """
        # OpenWeatherMap's historical API requires a paid subscription
        # For this demo, we'll simulate historical data
        return self._simulate_historical_data(start_date, end_date)

    def _simulate_historical_data(self, start_date, end_date):
        """Simulate historical weather data for demonstration"""
        import random
        import numpy as np

        current = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        historical_data = []
        base_temp = 15  # Base temperature in Celsius

        while current <= end:
            # Simulate temperature with some seasonality
            day_of_year = current.timetuple().tm_yday
            seasonal_temp = base_temp + 10 * np.sin(2 * np.pi * day_of_year / 365)
            temp = seasonal_temp + random.uniform(-5, 5)

            # Simulate weather conditions
            conditions = ["Clear", "Clouds", "Rain", "Drizzle", "Mist"]
            weights = [0.4, 0.3, 0.15, 0.1, 0.05]
            condition = random.choices(conditions, weights=weights)[0]

            historical_data.append({
                "date": current.strftime("%Y-%m-%d"),
                "temp": round(temp, 1),
                "condition": condition,
                "humidity": random.randint(40, 90),
                "wind_speed": round(random.uniform(0, 15), 1)
            })

            current += timedelta(days=1)

        return historical_data

    def parse_current_weather(self, data):
        """Parse current weather data"""
        if "error" in data:
            return None

        return {
            "city": data.get("name", "Unknown"),
            "country": data.get("sys", {}).get("country", ""),
            "temp": data.get("main", {}).get("temp", 0),
            "feels_like": data.get("main", {}).get("feels_like", 0),
            "temp_min": data.get("main", {}).get("temp_min", 0),
            "temp_max": data.get("main", {}).get("temp_max", 0),
            "humidity": data.get("main", {}).get("humidity", 0),
            "pressure": data.get("main", {}).get("pressure", 0),
            "wind_speed": data.get("wind", {}).get("speed", 0),
            "description": data.get("weather", [{}])[0].get("description", ""),
            "condition": data.get("weather", [{}])[0].get("main", ""),
            "icon": data.get("weather", [{}])[0].get("icon", ""),
            "timestamp": datetime.fromtimestamp(data.get("dt", 0))
        }

    def parse_forecast(self, data):
        """Parse forecast data"""
        if "error" in data:
            return None

        forecast_list = []
        for item in data.get("list", []):
            forecast_list.append({
                "datetime": datetime.fromtimestamp(item.get("dt", 0)),
                "temp": item.get("main", {}).get("temp", 0),
                "temp_min": item.get("main", {}).get("temp_min", 0),
                "temp_max": item.get("main", {}).get("temp_max", 0),
                "humidity": item.get("main", {}).get("humidity", 0),
                "description": item.get("weather", [{}])[0].get("description", ""),
                "condition": item.get("weather", [{}])[0].get("main", ""),
                "wind_speed": item.get("wind", {}).get("speed", 0),
            })

        return {
            "city": data.get("city", {}).get("name", "Unknown"),
            "country": data.get("city", {}).get("country", ""),
            "forecast": forecast_list
        }
