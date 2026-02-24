import requests
import os
from dotenv import load_dotenv

load_dotenv()

GEOCODE_API_KEY = os.getenv("GEOCODE_API_KEY")

def get_coordinates(address: str):
    """
    Fetch latitude and longitude using geocode.maps.co API
    """

    if not GEOCODE_API_KEY:
        raise ValueError("GEOCODE_API_KEY not found in environment variables")

    url = "https://geocode.maps.co/search"
    params = {
        "q": address,
        "api_key": GEOCODE_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data:
            print("No results found.")
            return None

        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])

        print(f"Latitude: {lat}, Longitude: {lon}")
        return lat, lon

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

get_coordinates("New York City")