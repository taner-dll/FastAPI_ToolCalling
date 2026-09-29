import os
import json
from collections.abc import Callable
from typing import Any


from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI

from tool_definitions import CITY_FOOD_TOOL, WEATHER_TOOL
from tools import get_city_food, get_weather

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4.1-nano"
MAX_TOOL_ROUNDS = 5
TOOLS = [WEATHER_TOOL, CITY_FOOD_TOOL]
AVAILABLE_TOOLS: dict[str, Callable[..., dict[str, object]]] = {
    "get_weather": get_weather,
    "get_city_food": get_city_food,
}


class ChatRequest(BaseModel):
    message: str


def execute_tool_call(name: str, arguments: str, call_id: str) -> dict[str, str]:
    """Execute a model-requested tool and format its output for Responses API."""
    tool = AVAILABLE_TOOLS.get(name)
    if tool is None:
        return {
            "type": "function_call_output",
            "call_id": call_id,
            "output": json.dumps({"error": f"Unknown tool: {name}"}),
        }

    try:
        parsed_arguments: Any = json.loads(arguments)
        if not isinstance(parsed_arguments, dict):
            raise ValueError("Tool arguments must be a JSON object.")

        result = tool(**parsed_arguments)
        output = json.dumps(result, ensure_ascii=False)
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        output = json.dumps({"error": str(exc)}, ensure_ascii=False)

    return {
        "type": "function_call_output",
        "call_id": call_id,
        "output": output,
    }


@app.post("/chat")
def chat(request: ChatRequest):
    response = client.responses.create(
        model=MODEL,
        input=request.message,
        tools=TOOLS,  # type: ignore[arg-type]
    )

    for _ in range(MAX_TOOL_ROUNDS):
        function_calls = [
            item for item in response.output if item.type == "function_call"
        ]
        if not function_calls:
            return {"response": response.output_text}

        tool_outputs = [
            execute_tool_call(item.name, item.arguments, item.call_id)
            for item in function_calls
        ]
        response = client.responses.create(
            model=MODEL,
            tools=TOOLS,  # type: ignore[arg-type]
            previous_response_id=response.id,
            input=tool_outputs,  # type: ignore[arg-type]
        )

    raise HTTPException(
        status_code=502,
        detail="The model exceeded the maximum number of tool-call rounds.",
    )


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Tool Calling Application!"}


