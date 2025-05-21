import os
import time
import random
import requests
from rektroid_bot import RektroidBot
import tweepy

# Setup Twitter API
def get_twitter_api():
    try:
        auth = tweepy.OAuthHandler(os.getenv("API_KEY"), os.getenv("API_SECRET"))
        auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))
        return tweepy.API(auth)
    except Exception as e:
        print(f"Twitter auth failed: {e}")
        return None

# Send logs to Discord via webhook
def discord_notify(message):
    webhook_url = os.getenv("DISCORD_LOG_WEBHOOK")
    if not webhook_url:
        print("No Discord webhook set for logging.")
        return
    try:
        requests.post(webhook_url, json={"content": message})
    except Exception as e:
        print(f"Failed to send Discord log: {e}")

# Setup the bot
rektroid = RektroidBot(api=get_twitter_api(), llm_api_key=os.getenv("OPENROUTER_API_KEY"))

# Auto roast scheduler
while True:
    try:
        roast, result = rektroid.auto_post_roast()
        discord_notify(f"🧠 Scheduled auto-roast:\n{roast}\n✅ {result}")
    except Exception as e:
        discord_notify(f"❌ Scheduler crashed: {e}")

    # Wait 1 hour + up to 10 mins
    delay = 3600 + random.randint(0, 600)
    time.sleep(delay)
