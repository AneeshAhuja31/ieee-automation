from instagrapi import Client
import time
import os
import requests
from dotenv import load_dotenv
load_dotenv(override=True)

print("start")
cl = Client()


SESSION_FILE = os.getenv("SESSION_FILE")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
TARGET_USER = os.getenv("TARGET_USER")
DOWNLOAD_FOLDER = "downloads"
MAX_POSTS = 45
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

#this is a working test, service to be created further on
try:
    if os.path.exists(SESSION_FILE):
        print("Loading saved session...")
        cl.load_settings(SESSION_FILE)
        try:
            cl.get_timeline_feed()
            print("Session loaded successfully.")
        except Exception:
            print("Saved session invalid, logging in again...")
            cl.login(USERNAME, PASSWORD)
            cl.dump_settings(SESSION_FILE)
            print("New session saved.")
    else:
        print("No saved session, logging in...")
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings(SESSION_FILE)
        print("Session saved.")

    print("Waiting 100-120 secs after login/session...")
    cl.delay_range = [100,120]

    user_id = cl.user_id_from_username(TARGET_USER)
    print("Waiting 60-70 secs before fetching posts...")
    cl.delay_range = [60,70]

    post_count = 0

    medias = cl.user_medias(user_id, amount=MAX_POSTS)

    for i, media in enumerate(medias, 1):
        print(f"\nPost {i}")
        print(f"Shortcode: {media.code}")
        print(f"Date: {media.taken_at}")
        print(f"Likes: {media.like_count}")
        print(f"Date: {media.taken_at}")
        print(f"Comments: {media.comment_count}")
        print(f"Caption: {media.caption_text or 'No caption'}")
        print(f"Post URL: https://www.instagram.com/p/{media.code}/")

        if media.media_type == 1:  # Image
            
            img_url = media.thumbnail_url
            new_dir = os.path.join(DOWNLOAD_FOLDER,"post_"+media.taken_at)
            os.makedirs(new_dir,exist_ok=True)
            img_data = cl.photo_download(media.pk, folder=new_dir)
            print(f"Saved Image: {img_data}")
            
        elif media.media_type == 8:  # Carousel
            print(f"Post {i} is a carousel, downloading first image only.")
            new_dir = os.path.join(DOWNLOAD_FOLDER,"post_"+media.taken_at)
            os.makedirs(new_dir,exist_ok=True)
            for item in media.resources:
                img_url = item.thumbnail_url

                img_data = cl.photo_download(item.pk,folder=new_dir)
                print(f"Saved Image: {img_data}")
                print("Sleeping 10-20 secs")
                cl.delay_range = [10,20]
        else:
            print("Other media type, skipping.")

        post_count += 1
        if i < MAX_POSTS:
            print("Waiting 30 seconds before next post...")
            cl.delay_range = [30,60]

    print(f"\nSuccessfully processed {post_count} posts.")

except Exception as e:
    print(f"Error: {e}")
    if "login" in str(e).lower():
        print("Check login credentials.")
    elif "wait" in str(e).lower():
        print("Rate limited!")
    else:
        print(e)

finally:
    print("Script completed.")