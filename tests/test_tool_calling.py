import json
import os
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

os.environ.setdefault("OPENAI_API_KEY", "test-key")

import main
from tools import get_city_food, get_weather


class ChatTests(unittest.TestCase):
    def test_returns_direct_model_response(self):
        response = SimpleNamespace(id="response-1", output=[], output_text="Merhaba")

        with patch.object(main.client.responses, "create", return_value=response):
            result = main.chat(main.ChatRequest(message="Selam"))

        self.assertEqual(result, {"response": "Merhaba"})

    def test_executes_tool_and_returns_follow_up_response(self):
        function_call = SimpleNamespace(
            type="function_call",
            name="get_weather",
            arguments='{"city":"Istanbul"}',
            call_id="call-1",
        )
        first_response = SimpleNamespace(
            id="response-1",
            output=[function_call],
            output_text="",
        )
        final_response = SimpleNamespace(
            id="response-2",
            output=[],
            output_text="Istanbul 22 derece ve bulutlu.",
        )
        create = Mock(side_effect=[first_response, final_response])

        with patch.object(main.client.responses, "create", create):
            result = main.chat(main.ChatRequest(message="Istanbul'da hava nasil?"))

        self.assertEqual(result, {"response": "Istanbul 22 derece ve bulutlu."})
        continuation = create.call_args_list[1].kwargs
        tool_output = continuation["input"][0]
        self.assertEqual(continuation["previous_response_id"], "response-1")
        self.assertEqual(tool_output["call_id"], "call-1")
        self.assertEqual(
            json.loads(tool_output["output"]),
            {
                "city": "Istanbul",
                "available": True,
                "temperature": 22,
                "condition": "cloudy",
            },
        )

    def test_executes_multiple_tools_in_the_same_round(self):
        weather_call = SimpleNamespace(
            type="function_call",
            name="get_weather",
            arguments='{"city":"Izmir"}',
            call_id="weather-call",
        )
        food_call = SimpleNamespace(
            type="function_call",
            name="get_city_food",
            arguments='{"city":"Izmir"}',
            call_id="food-call",
        )
        first_response = SimpleNamespace(
            id="response-1",
            output=[weather_call, food_call],
            output_text="",
        )
        final_response = SimpleNamespace(
            id="response-2",
            output=[],
            output_text="Izmir gunesli ve meshur yemegi boyoz.",
        )
        create = Mock(side_effect=[first_response, final_response])

        with patch.object(main.client.responses, "create", create):
            result = main.chat(
                main.ChatRequest(message="Izmir'in havasi ve meshur yemegi nedir?")
            )

        self.assertEqual(
            result,
            {"response": "Izmir gunesli ve meshur yemegi boyoz."},
        )
        tool_outputs = create.call_args_list[1].kwargs["input"]
        self.assertEqual(
            [tool_output["call_id"] for tool_output in tool_outputs],
            ["weather-call", "food-call"],
        )


class WeatherToolTests(unittest.TestCase):
    def test_city_lookup_is_case_insensitive(self):
        self.assertTrue(get_weather("  ANKARA  ")["available"])

    def test_unknown_city_has_consistent_unavailable_result(self):
        result = get_weather("Bursa")

        self.assertEqual(result["city"], "Bursa")
        self.assertFalse(result["available"])


class CityFoodToolTests(unittest.TestCase):
    def test_city_food_lookup_is_case_insensitive(self):
        result = get_city_food("  IZMIR  ")

        self.assertTrue(result["available"])
        self.assertEqual(result["food"], "Boyoz")

    def test_unknown_city_has_consistent_unavailable_result(self):
        result = get_city_food("Bursa")

        self.assertEqual(result["city"], "Bursa")
        self.assertFalse(result["available"])


if __name__ == "__main__":
    unittest.main()
