import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv
load_dotenv(override=True)

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

async def upload_to_cloudinary(url):
    result = cloudinary.uploader.upload(url)
    return result.get("secure_url")