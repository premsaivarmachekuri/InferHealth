import requests
from app.core.config import settings

def get_coordinates(address: str):
    """
    Fetch latitude and longitude using geocode.maps.co API.
    Used for locating hospitals relative to the user.
    """
    if not settings.GEOCODE_API_KEY:
        print("Warning: GEOCODE_API_KEY not found.")
        return None

    url = "https://geocode.maps.co/search"
    params = {
        "q": address,
        "api_key": settings.GEOCODE_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data:
            return None

        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return lat, lon

    except Exception as e:
        print(f"Geocoding failed: {e}")
        return None
