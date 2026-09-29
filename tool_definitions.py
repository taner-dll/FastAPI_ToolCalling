WEATHER_TOOL = {
    "type": "function",
    "name": "get_weather",
    "description": "Get the weather for a given city.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The name of the city for which to get the weather."
            }
        },
        "required": ["city"],
        "additionalProperties": False
    },
    "strict": True
}


CITY_FOOD_TOOL = {
    "type": "function",
    "name": "get_city_food",
    "description": "Get a well-known food for a given city.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The name of the city for which to get food information."
            }
        },
        "required": ["city"],
        "additionalProperties": False
    },
    "strict": True
}
