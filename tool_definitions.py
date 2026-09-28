WEATHER_TOOL = {
    "type": "function",
    "name": "Weather Tool",
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