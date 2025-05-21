from flask import Flask, request, jsonify
import os
from rektroid_bot import RektroidBot  # Assuming your class is saved in rektroid_bot.py
import tweepy

app = Flask(__name__)

# Load secrets from environment
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")


def get_twitter_api():
    try:
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return tweepy.API(auth)
    except Exception as e:
        print(f"Twitter auth failed: {e}")
        return None


bot = RektroidBot(api=get_twitter_api())


@app.route("/roast", methods=["POST"])
def manual_roast():
    data = request.get_json()
    community = data.get("community", "")
    roast = bot.generate_roast(community)
    return jsonify({"community": community, "roast": roast})


@app.route("/roast/post", methods=["POST"])
def roast_and_post():
    data = request.get_json()
    community = data.get("community", "")
    roast = bot.generate_roast(community)
    result = bot.post_roast(roast)
    return jsonify({"community": community, "roast": roast, "result": result})


@app.route("/roast/auto", methods=["GET"])
def auto_roast():
    roast, result = bot.auto_post_roast()
    return jsonify({"auto_roast": roast, "result": result})


@app.route("/roast/llm", methods=["POST"])
def llm_roast():
    data = request.get_json()
    community = data.get("community", "")
    roast = bot.generate_llm_roast(community)
    return jsonify({"llm_roast": roast})


@app.route("/", methods=["GET"])
def home():
    return "REKTroid bot is running."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
