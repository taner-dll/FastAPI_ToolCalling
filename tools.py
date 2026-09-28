

def get_weather(city: str) -> str:
    """Get the weather for a given city.

    Args:
        city (str): The name of the city for which to get the weather.

    Returns:
        str: A description of the weather in the specified city.
    """
    
    weather_data = {
        "istanbul": {
            "temperature": 22,
            "condition": "cloudy"
        },
        "ankara": {
            "temperature": 18,
            "condition": "sunny"
        },
        "izmir": {
            "temperature": 27,
            "condition": "sunny"
        }
    }
    
    
    return weather_data.get(city, {"description": "Weather data not available", "temperature": "N/A", "humidity": "N/A", "wind_speed": "N/A"}) # type: ignore


