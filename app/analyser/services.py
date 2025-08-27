from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage,SystemMessage
from dotenv import load_dotenv
import os
import httpx
import requests
import base64
from analyser.schemas import EventInfo, CleanedJSON
from analyser.prompt import system_prompt
from analyser.api_key_manager import APIKeyManager
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

async def llm_call(cleaned_json: CleanedJSON):
    img_b64 = await get_b64(cleaned_json.url)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=api_key_manager.get_next_key())
    structured_llm = llm.with_structured_output(EventInfo)

    messages = [
        SystemMessage(content=(
            system_prompt
        )),
        HumanMessage(content=[
            {"type": "text", "text": cleaned_json.caption},
            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{img_b64}"}
        ])
    ]

    response = structured_llm.invoke(messages)
    print("Extracted JSON:\n", response)
    return response

def get_b64_(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    image_bytes = response.content
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    return image_b64


def llm_call_(cleaned_json: CleanedJSON):
    img_b64 = get_b64_(cleaned_json.url)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=api_key_manager.get_next_key())

    structured_llm = llm.with_structured_output(EventInfo)

    messages = [
        SystemMessage(content=(
            system_prompt
        )),
        HumanMessage(content=[
            {"type": "text", "text": cleaned_json.caption},
            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{img_b64}"}
        ])
    ]

    response = structured_llm.invoke(messages)
    print("Extracted JSON:\n", response) 
    return response

llm_call_(CleanedJSON(
    url="https://instagram.fdel27-5.fna.fbcdn.net/v/t51.2885-15/479737783_18146646982371039_4487077495262782556_n.jpg?stp=dst-jpg_e35_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0uaW1hZ2VfdXJsZ2VuLjEwODB4MTM1MC5zZHIuZjc1NzYxLmRlZmF1bHRfaW1hZ2UuYzIifQ&_nc_ht=instagram.fdel27-5.fna.fbcdn.net&_nc_cat=103&_nc_oc=Q6cZ2QFV2cBmF-P23oKeLsj1fRxNAIgG1TyhezSRNGFRxYG9coSypF3Vokp6gVPkEBfjRpA6bAl9f6PS9z_vpoqoShiW&_nc_ohc=ia54c7z5_zUQ7kNvwGpionn&_nc_gid=RakLwC3kYOrlN4JnjeovDQ&edm=AP4sbd4BAAAA&ccb=7-5&ig_cache_key=MzU2OTMzMjU4MjAzODYzMzY5MA%3D%3D.3-ccb7-5&oh=00_AfWqu84LbRZ9KlkQ1M5uE3puRz5Jxdu04HO0GPKa14GtAA&oe=68B55F60&_nc_sid=7a9f4b",
    caption="🌟 Presenting the 𝐀𝐃𝐕𝐈𝐒𝐎𝐑𝐒 of 𝐈𝐄𝐄𝐄 𝐌𝐒𝐈𝐓 for the 𝟐𝟎𝟐𝟓-𝟐𝟎𝟐𝟔 𝘁𝗲𝗻𝘂𝗿𝗲! ❤️💫\n\nYour 𝐠𝐮𝐢𝐝𝐚𝐧𝐜𝐞,𝐰𝐢𝐬𝐝𝐨𝐦, and 𝐞𝐱𝐩𝐞𝐫𝐢𝐞𝐧𝐜𝐞 lay the foundation of our journey.\n\nWith your support, we strive to learn and innovate, ensuring that 𝐈𝐄𝐄𝐄 𝐌𝐒𝐈𝐓 soars to new heights. ✨🙌🏻\n\n𝘎𝘳𝘦𝘢𝘵 𝘭𝘦𝘢𝘥𝘦𝘳𝘴 𝘥𝘰𝘯'𝘵 𝘫𝘶𝘴𝘵 𝘴𝘦𝘵 𝘵𝘩𝘦 𝘱𝘢𝘵𝘩, 𝘵𝘩𝘦𝘺 𝘪𝘭𝘭𝘶𝘮𝘪𝘯𝘢𝘵𝘦 𝘪𝘵 𝘧𝘰𝘳 𝘰𝘵𝘩𝘦𝘳𝘴 𝘵𝘰 𝘧𝘰𝘭𝘭𝘰𝘸. 💫\n\nDesigned By: @thatcoffeeaddictedpookie @shauryaguptaaaa\n\n#IEEEAdvisory2025 #LearningFromTheBest #GuidedByWisdom #IEEE #IEEEMSIT"
))
