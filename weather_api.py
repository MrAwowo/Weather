import requests
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

class WeatherAPI:
    """
    Fetch weather data from Open-Meteo (truly public, no API key needed)
    Open-Meteo: https://open-meteo.com/
    """

    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1"
        self.geocoder = Nominatim(user_agent="weather_prediction_app")

    def _get_coordinates(self, city, country_code=""):
        """Get latitude and longitude for a city"""
        try:
            location_query = f"{city}, {country_code}" if country_code else city
            location = self.geocoder.geocode(location_query, timeout=15)

            if location:
                return {
                    "lat": location.latitude,
                    "lon": location.longitude,
                    "display_name": location.address
                }

            # If first attempt fails, try without country code
            if country_code:
                location = self.geocoder.geocode(city, timeout=15)
                if location:
                    return {
                        "lat": location.latitude,
                        "lon": location.longitude,
                        "display_name": location.address
                    }

            return None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            # Try one more time without country code
            try:
                location = self.geocoder.geocode(city, timeout=15)
                if location:
                    return {
                        "lat": location.latitude,
                        "lon": location.longitude,
                        "display_name": location.address
                    }
            except:
                pass
            return None

    def get_current_weather(self, city, country_code=""):
        """Get current weather for a city"""
        try:
            # Get coordinates
            coords = self._get_coordinates(city, country_code)
            if not coords:
                return {"error": f"Could not find location: {city}"}

            # Fetch current weather from Open-Meteo
            url = f"{self.base_url}/forecast"
            params = {
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,surface_pressure,wind_speed_10m",
                "timezone": "auto"
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Add location info
            data["location"] = {
                "city": city,
                "country": country_code,
                "lat": coords["lat"],
                "lon": coords["lon"]
            }

            return data

        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_forecast(self, city, country_code="", days=7):
        """Get weather forecast for a city (up to 16 days)"""
        try:
            # Get coordinates
            coords = self._get_coordinates(city, country_code)
            if not coords:
                return {"error": f"Could not find location: {city}"}

            # Fetch forecast from Open-Meteo
            url = f"{self.base_url}/forecast"
            params = {
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "daily": "temperature_2m_max,temperature_2m_min,weather_code,precipitation_sum,wind_speed_10m_max",
                "timezone": "auto",
                "forecast_days": min(days, 16)
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Add location info
            data["location"] = {
                "city": city,
                "country": country_code,
                "lat": coords["lat"],
                "lon": coords["lon"]
            }

            return data

        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_historical_data(self, city, country_code, start_date, end_date):
        """
        Get REAL historical weather data from Open-Meteo
        This is truly public and free - no API key needed!
        """
        try:
            # Get coordinates
            coords = self._get_coordinates(city, country_code)
            if not coords:
                return []

            # Open-Meteo historical API
            url = "https://archive-api.open-meteo.com/v1/archive"
            params = {
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "start_date": start_date,
                "end_date": end_date,
                "daily": "temperature_2m_mean,weather_code,relative_humidity_2m_mean,wind_speed_10m_mean",
                "timezone": "auto"
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Parse historical data
            historical_data = []
            daily = data.get("daily", {})
            dates = daily.get("time", [])
            temps = daily.get("temperature_2m_mean", [])
            weather_codes = daily.get("weather_code", [])
            humidity = daily.get("relative_humidity_2m_mean", [])
            wind_speeds = daily.get("wind_speed_10m_mean", [])

            for i in range(len(dates)):
                historical_data.append({
                    "date": dates[i],
                    "temp": temps[i] if i < len(temps) else 0,
                    "condition": self._weather_code_to_condition(weather_codes[i] if i < len(weather_codes) else 0),
                    "humidity": humidity[i] if i < len(humidity) else 0,
                    "wind_speed": wind_speeds[i] if i < len(wind_speeds) else 0
                })

            return historical_data

        except Exception as e:
            import traceback
            error_msg = f"Error fetching historical data: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)  # For server logs
            raise Exception(f"Failed to fetch historical data: {str(e)}")

    def _weather_code_to_condition(self, code):
        """Convert WMO weather code to condition string"""
        # WMO Weather interpretation codes
        if code == 0:
            return "Clear"
        elif code in [1, 2, 3]:
            return "Clouds"
        elif code in [45, 48]:
            return "Fog"
        elif code in [51, 53, 55, 56, 57]:
            return "Drizzle"
        elif code in [61, 63, 65, 66, 67, 80, 81, 82]:
            return "Rain"
        elif code in [71, 73, 75, 77, 85, 86]:
            return "Snow"
        elif code in [95, 96, 99]:
            return "Thunderstorm"
        else:
            return "Clear"

    def _weather_code_to_description(self, code):
        """Convert WMO weather code to detailed description"""
        descriptions = {
            0: "clear sky",
            1: "mainly clear",
            2: "partly cloudy",
            3: "overcast",
            45: "fog",
            48: "depositing rime fog",
            51: "light drizzle",
            53: "moderate drizzle",
            55: "dense drizzle",
            61: "slight rain",
            63: "moderate rain",
            65: "heavy rain",
            71: "slight snow",
            73: "moderate snow",
            75: "heavy snow",
            80: "slight rain showers",
            81: "moderate rain showers",
            82: "violent rain showers",
            95: "thunderstorm",
            96: "thunderstorm with slight hail",
            99: "thunderstorm with heavy hail"
        }
        return descriptions.get(code, "clear sky")

    def parse_current_weather(self, data):
        """Parse current weather data from Open-Meteo"""
        if "error" in data:
            return None

        current = data.get("current", {})
        location = data.get("location", {})

        weather_code = current.get("weather_code", 0)

        return {
            "city": location.get("city", "Unknown"),
            "country": location.get("country", ""),
            "temp": current.get("temperature_2m", 0),
            "feels_like": current.get("apparent_temperature", 0),
            "temp_min": current.get("temperature_2m", 0),  # Current doesn't have min/max
            "temp_max": current.get("temperature_2m", 0),
            "humidity": current.get("relative_humidity_2m", 0),
            "pressure": current.get("surface_pressure", 0),
            "wind_speed": current.get("wind_speed_10m", 0),
            "description": self._weather_code_to_description(weather_code),
            "condition": self._weather_code_to_condition(weather_code),
            "icon": str(weather_code),
            "timestamp": datetime.now()
        }

    def parse_forecast(self, data):
        """Parse forecast data from Open-Meteo"""
        if "error" in data:
            return None

        daily = data.get("daily", {})
        location = data.get("location", {})

        forecast_list = []
        dates = daily.get("time", [])
        temps_max = daily.get("temperature_2m_max", [])
        temps_min = daily.get("temperature_2m_min", [])
        weather_codes = daily.get("weather_code", [])
        wind_speeds = daily.get("wind_speed_10m_max", [])

        for i in range(len(dates)):
            temp_max = temps_max[i] if i < len(temps_max) else 0
            temp_min = temps_min[i] if i < len(temps_min) else 0
            temp_avg = (temp_max + temp_min) / 2
            weather_code = weather_codes[i] if i < len(weather_codes) else 0

            forecast_list.append({
                "datetime": datetime.fromisoformat(dates[i]),
                "temp": temp_avg,
                "temp_min": temp_min,
                "temp_max": temp_max,
                "humidity": 0,  # Not available in daily forecast
                "description": self._weather_code_to_description(weather_code),
                "condition": self._weather_code_to_condition(weather_code),
                "wind_speed": wind_speeds[i] if i < len(wind_speeds) else 0,
            })

        return {
            "city": location.get("city", "Unknown"),
            "country": location.get("country", ""),
            "forecast": forecast_list
        }
