from geopy import Nominatim
from ..task import Task
import requests


class WeatherTask(Task):

    def __init__(self, name, keywords: list[str], description: str):
        super().__init__(name, keywords, description)

    def execute(self, parameters=None):
        if parameters is not None:
            gpt = parameters['gpt']
            location = self.extract_task_params("Extract the location mentioned here in one word", gpt)
            geolocator = Nominatim(user_agent="UnityXV")
            location_coords = geolocator.geocode(location)
            if location_coords is not None:
                url = "https://api.open-meteo.com/v1/forecast"
                params = {
                    "latitude": location_coords.latitude,  # Latitude for London
                    "longitude": location_coords.longitude,  # Longitude for London
                    "hourly": "temperature_2m",  # Get temperature data at 2 meters
                    "current_weather": True,  # Get current weather data
                }
                # Make a GET request to the Open-Meteo API
                response = requests.get(url, params=params)
                # Convert the response to JSON
                weather_data = response.json()
                print(weather_data)
                return weather_data
            else:
                return "I could not find this place anywhere, did you just make that up?"