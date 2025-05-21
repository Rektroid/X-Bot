import json
import logging
import random
from datetime import datetime
from typing import List, Dict, Optional
import requests

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Optional: spaCy not used here to avoid memory issues
# import spacy
# nlp = spacy.load("en_core_web_sm")

class RektroidBot:
    def __init__(self, api=None, llm_api_key=None, history_file="roast_history.jsonl"):
        self.api = api
        self.llm_api_key = llm_api_key
        self.analyzer = SentimentIntensityAnalyzer()
        self.history_file = history_file
        self.roast_templates = self.load_templates()
        self.x_post_mentions = {k: [] for k in self.roast_templates.keys()}
        self.query_map = self.create_query_map()
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def load_templates(self) -> Dict[str, List[str]]:
        return {
            "hypio holders": [
                "Yo {community}, your Hypio Babies are such garbage, they’re worth less than a rugpull’s fart!",
                "Bridging to HyperEVM for airdrops? {community}, your wallet’s so dry it’s shittier than a JPEG scam!",
            ],
            "hyperliquid maxxis": [
                "Farming HYPE like a sweaty bot, {community}? Your yields are so bad, a piggy bank outperforms!",
                "Calling Hyperliquid ‘on-chain Binance’? {community}, your trades lag like a 90s modem!",
            ],
            "rektroid": [
                "I’m REKTroid, $REKT, torching degens like it’s my fucking job! Suck my dick!",
                "Fuck yeah, I’m REKTroid, scraping X faster than you chase $PURR airdrops! Hit me up, dumbass!",
            ],
        }

    def create_query_map(self) -> Dict[str, str]:
        return {
            "hypio holders": "Hypio Babies",
            "hyperliquid maxxis": "Hyperliquid",
            "rektroid": "REKTroid",
        }

    def scrape_x_posts(self, community: str, query: str, max_posts: int = 10) -> List[Dict]:
        if self.api is None:
            logging.warning("API not available for scraping.")
            return []

        try:
            search_query = f"{query} -filter:retweets"
            tweets = self.api.search_tweets(q=search_query, lang="en", count=max_posts, tweet_mode="extended")
            results = []
            for tweet in tweets:
                text = tweet.full_text if hasattr(tweet, 'full_text') else tweet.text
                sentiment = self.analyzer.polarity_scores(text)
                results.append({
                    "text": text,
                    "sentiment": sentiment['compound'],
                    "user": tweet.user.screen_name
                })
            return results
        except Exception as e:
            logging.error(f"Scraping failed for {query}: {e}")
            return []

    def extract_phrases(self, text: str) -> List[str]:
        # Simple fallback without spaCy
        return [match.group(0) for match in re.finditer(r"\b\w+\s+\w+\b", text)]

    def generate_dynamic_roast(self, community: str, posts: List[Dict]) -> str:
        community_key = community.lower()
        if not posts:
            return random.choice(self.roast_templates.get(community_key, ["No fresh X data."])).format(
                community=community.capitalize())

        bullish_phrases = []
        bearish_phrases = []
        for post in posts:
            sentiment = post["sentiment"]
            phrases = self.extract_phrases(post["text"])
            if sentiment > 0.2:
                bullish_phrases.extend(phrases)
            elif sentiment < -0.2:
                bearish_phrases.extend(phrases)

        if bullish_phrases and random.random() < 0.6:
            phrase = random.choice(bullish_phrases)
            roast = f"Degens shilling '{phrase}' for {community.capitalize()}? Your hype’s shittier than a rugpull!"
        elif bearish_phrases:
            phrase = random.choice(bearish_phrases)
            roast = f"X is whining about '{phrase}' in {community.capitalize()}? Bags so rekt, even bots won’t touch them!"
        else:
            roast = f"X is quiet on {community.capitalize()} — your bags are deader than a testnet!"

        self.x_post_mentions[community_key].append(roast)
        self.save_roast(community, roast)
        return roast

    def generate_roast(self, community: str) -> str:
        community_key = community.lower()
        if community_key not in self.roast_templates:
            return f"No roasts for {community}. Try another known degen crew."

        query = self.query_map.get(community_key, community_key)
        posts = self.scrape_x_posts(community_key, query)

        if posts and random.random() < 0.7:
            return self.generate_dynamic_roast(community_key, posts)
        elif self.x_post_mentions[community_key] and random.random() < 0.6:
            return random.choice(self.x_post_mentions[community_key])
        else:
            roast = random.choice(self.roast_templates[community_key]).format(community=community.capitalize())
            self.save_roast(community, roast)
            return roast

    def save_roast(self, community: str, roast: str):
        with open(self.history_file, "a") as f:
            json.dump({
                "timestamp": datetime.utcnow().isoformat(),
                "community": community,
                "roast": roast
            }, f)
            f.write("\n")

    def post_roast(self, roast: str) -> str:
        if self.api is None:
            return "Can't post: API unavailable."
        try:
            self.api.update_status(roast)
            logging.info(f"Posted roast: {roast}")
            return "Roast posted successfully."
        except Exception as e:
            logging.error(f"Failed to post roast: {e}")
            return f"Failed to post: {e}"

    def generate_llm_roast(self, community: str, context: Optional[str] = "") -> str:
    prompt = f"Write a savage, degenerate crypto-style roast tweet targeting the '{community}' community. Be edgy and meme-heavy."
    try:
        headers = {
            "Authorization": f"Bearer {self.llm_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "openrouter/cinematika:free",  # or any other free model
            "messages": [
                {"role": "system", "content": "You are REKTroid, a ruthless AI crypto roaster."},
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        roast = response.json()["choices"][0]["message"]["content"]
        return roast
    except Exception as e:
        return f"LLM failed to generate roast: {e}"

    def auto_post_roast(self):
        top_communities = list(self.roast_templates.keys())
        community = random.choice(top_communities)
        roast = self.generate_roast(community)
        result = self.post_roast(roast)
        return roast, result
