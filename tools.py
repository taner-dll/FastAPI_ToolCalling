def get_weather(city: str) -> dict[str, object]:
    """Get the weather for a given city.

    Args:
        city (str): The name of the city for which to get the weather.

    Returns:
        dict: Demo weather data for the specified city.
    """
    weather_data = {
        "istanbul": {
            "temperature": 22,
            "condition": "cloudy",
        },
        "ankara": {
            "temperature": 18,
            "condition": "sunny",
        },
        "izmir": {
            "temperature": 27,
            "condition": "sunny",
        },
    }

    normalized_city = city.strip().casefold()
    weather = weather_data.get(normalized_city)
    if weather is None:
        return {
            "city": city.strip(),
            "available": False,
            "message": "Weather data not available",
        }

    return {
        "city": normalized_city.title(),
        "available": True,
        **weather,
    }


def get_city_food(city: str) -> dict[str, object]:
    """Get a well-known food for a given city."""
    city_foods = {
        "istanbul": "Balik ekmek",
        "ankara": "Ankara tava",
        "izmir": "Boyoz",
    }

    normalized_city = city.strip().casefold()
    food = city_foods.get(normalized_city)
    if food is None:
        return {
            "city": city.strip(),
            "available": False,
            "message": "City food data not available",
        }

    return {
        "city": normalized_city.title(),
        "available": True,
        "food": food,
    }
