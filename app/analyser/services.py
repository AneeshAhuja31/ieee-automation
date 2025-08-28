from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage,SystemMessage
from dotenv import load_dotenv
import os
import httpx
import requests
import base64
from analyser.schemas import EventInfo, CleanedJSON, IsSame
from analyser.prompt import system_prompt,isSame_system_prompt
from analyser.api_key_manager import APIKeyManager
from datetime import datetime
api_key_manager = APIKeyManager()
load_dotenv(override=True)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

async def get_b64(url:str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    image_bytes = response.content
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    return image_b64

async def llm_call(cleaned_json: CleanedJSON) -> EventInfo:
    img_b64 = await get_b64(cleaned_json.url)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=api_key_manager.get_next_key())
    structured_llm = llm.with_structured_output(EventInfo)

    messages = [
        SystemMessage(content=(
            system_prompt
        )),
        HumanMessage(content=[
            {"type": "text", "text": cleaned_json.caption},
            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{img_b64}"},
            {"type": "text", "text": f"Current datetime: {datetime.utcnow()}"}
        ])
    ]

    response = structured_llm.invoke(messages)
    return response

async def check_if_description_is_same(desc1: str, desc2: str) -> bool:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key_manager.get_next_key())
    structured_llm = llm.with_structured_output(IsSame)
    messages = [
        SystemMessage(content=isSame_system_prompt),
        HumanMessage(content=[
            {"type": "text", "text": f"Event 1 Description: {desc1}"},
            {"type": "text", "text": f"Event 2 Description: {desc2}"}
        ])
    ]
    response = structured_llm.invoke(messages)
    print("------------------------------------")
    print(response.isSame)
    print("------------------------------------")
    return response.isSame


