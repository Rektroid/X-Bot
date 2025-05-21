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

# Community activity weights (higher = more posts)
ACTIVITY_WEIGHTS = {
    "hypio holders": 3.0,
    "alright buddy holders": 3.0,
    "$neko degens": 2.5,
    "$purr degens": 2.0,
    "pvp.trade degens": 2.0,
    "tinyhypercats degens": 1.5,
    "hyperliquid maxxis": 2.5,
    "$catbal holders": 2.0,
    "karu degens": 1.0,
    "drip trade": 1.5,
    "liquidscan degens": 1.0,
    "$sph800 holders": 0.5,
    "$pip holders": 0.5,
    "liquidlaunch degens": 1.5,
    "hfun/hypurr fun degens": 2.5,
    "hyperswap traders": 1.0,
    "$rub degens": 0.5,
    "rektroid": 1.0
}

# Auto roast scheduler
while True:
    try:
        # Weighted community selection
        communities = list(ACTIVITY_WEIGHTS.keys())
        weights = list(ACTIVITY_WEIGHTS.values())
        selected_community = random.choices(communities, weights=weights, k=1)[0]
        
        roast = rektroid.generate_roast(selected_community)
        result = rektroid.post_roast(roast)
        discord_notify(f"🧠 Scheduled auto-roast for **{selected_community}**:\n{roast}\n✅ {result}")

    except Exception as e:
        discord_notify(f"❌ Scheduler crashed: {e}")

    # Wait 1 hour + up to 10 mins
    delay = 3600 + random.randint(0, 600)
    time.sleep(delay)
