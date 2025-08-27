from instagrapi import Client
import time
import os
from dotenv import load_dotenv
load_dotenv()

print("start")

cl = Client()


SESSION_FILE = os.getenv("SESSION_FILE")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
TARGET_USER = os.getenv("TARGET_USER")

try:
    if os.path.exists(SESSION_FILE):
        print("loading saved session")
        cl.load_settings(SESSION_FILE)
        try:
            cl.get_timeline_feed()  
            print("session loaded successfully")
        except Exception:
            print("saved session invalid loggingin again")
            cl.login(USERNAME, PASSWORD)
            cl.dump_settings(SESSION_FILE)
            print("new session saved")
    else:
        print("no saved session, logging in...")
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings(SESSION_FILE)
        print("session saved")

    print("waiting 2 mins after login/session")
    time.sleep(120)

    user_id = cl.user_id_from_username(TARGET_USER)
    profile_info = cl.user_info(user_id)
    
    print(f"Profile: {profile_info.full_name}")
    print(f"Followers: {profile_info.follower_count}")
    print(f"Posts: {profile_info.media_count}")
    
    print("Waiting 1 min before fetching posts")
    time.sleep(60)
    
    post_count = 0
    max_posts = 3
    
    try:
        medias = cl.user_medias(user_id, amount=max_posts)
        
        for i, media in enumerate(medias, 1):
            print(f"\nPost {i}")
            print(f"Shortcode: {media.code}")
            print(f"Date: {media.taken_at}")
            print(f"Likes: {media.like_count}")
            print(f"Comments: {media.comment_count}")
            
            caption = media.caption_text or "No caption"
            print(f"Caption: {caption}")
            
            print(f"Post URL: https://www.instagram.com/p/{media.code}/")
            print(f"Media URL: {media.thumbnail_url}")
            
            post_count += 1
            
            if i < max_posts:
                print("waiting 30 seconds before next post")
                time.sleep(30)
    
    except Exception as post_error:
        print(f"error getting posts: {post_error}")
        if "wait" in str(post_error).lower():
            print("rate limited!")
        
    print(f"\nsuccessfully processed {post_count} posts")
    
except Exception as e:
    print(f"Error: {e}")
    if "login" in str(e).lower():
        print("check login credentials")
    elif "wait" in str(e).lower():
        print("Rate limited!")
    else:
        print(f"{e}")

finally:
    print("script completed")
