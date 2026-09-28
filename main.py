import os
import json


from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI

from tools import get_weather
from tool_definitions import WEATHER_TOOL

load_dotenv()

app = FastAPI()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))






@app.get("/")
async def root():
    print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
    return {"message": "Welcome to the FastAPI Tool Calling Application!"}


