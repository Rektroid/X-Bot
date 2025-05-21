import random
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import schedule
import time
import re
import logging

# X API credentials (replace with your Basic X API credentials from https://developer.x.com)
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_TOKEN_SECRET = "your_access_token_secret"

# Setup logging
logging.basicConfig(filename='roasts.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Savage roast templates for Hyperliquid Maxxis communities and REKTroid ($REKT)
ROAST_TEMPLATES = {
    "hypio holders": [
        "Yo {community}, your Wealthy Hypio Babies are such fucking garbage, they’re worth less than a rugpull’s fart! Suck my dick!",
        "Fuck, {community}, you’re bridging to HyperEVM for airdrops? Your wallet’s so dry it’s shittier than a $JPEG scam!",
        "{community}, your NFTs are deader than a fucking testnet! Even bots are like, ‘Suck my dick, I ain’t buying!’",
    ],
    "alright buddy holders": [
        "{community}, HODLing $BUDDY like it’s gonna 100x? Your bags are shittier than a HyperSwap dump! Suck my dick, degen!",
        "Fuckin’ {community}, your $BUDDY’s flatter than a rugpull’s promises! Quit shilling that trash!",
        "Yo {community}, your $BUDDY bags are screaming ‘fuck me’ louder than a bear market crash! Suck it!",
    ],
    "hyperliquid maxxis": [
        "{community}, farming HYPE airdrops like a sweaty bot? Your yields are so shit, a piggy bank fucks harder! Suck my dick!",
        "Fuck, {community}, you call Hyperliquid ‘on-chain Binance’? Your trades lag like a fucking 90s modem!",
        "Yo {community}, you’re so deep in HyperBFT, you forgot how to wipe your ass! Suck my dick, degen!",
    ],
    "drip trade": [
        "{community}, flipping Hypers NFTs like you’re a whale? Your JPEGs are worth less than a fuck! Suck my dick!",
        "Fuckin’ {community}, grinding Drip Trade for $JPEG? Your wallet’s emptier than a HyperEVM scam chain!",
        "Yo {community}, your ‘NFT exchange’ is just you getting fucked for overpaying pixels! Suck it!",
    ],
    "$sph800 holders": [
        "{community}, HODLing $SPH800 like it’s $HYPE? Your bags are shittier than a scam token! Suck my dick!",
        "Fuck, {community}, shilling $SPH800 on X? Your chart’s so dead, even bots say ‘fuck off’!",
        "Yo {community}, your $SPH800 dreams are getting fucked harder than a HyperSwap rug! Suck it!",
    ],
    "$pip holders": [
        "{community}, you chased $PIP’s $2M volume like a dumbass? Your bags are shittier than a flash crash! Suck my dick!",
        "Fuckin’ {community}, hyping $PIP like it’s gonna moon? It’s dumping harder than a shitty NFT mint! Suck it!",
        "Yo {community}, your $PIP HODL’s so pathetic, HyperEVM bots are like, ‘Fuck this, I’m out!’",
    ],
    "liquidlaunch degens": [
        "{community}, bidding on LiquidLaunch like you’re hot shit? Your $LIQD’s worth less than a fuck! Suck my dick!",
        "Fuck, {community}, camping LiquidLaunch for $BUDDY pumps? Your wallet’s stuck in a 31-hour rugpull!",
        "Yo {community}, LiquidLaunch’s ‘future’? Your tokens are deader than a fucking testnet! Suck it!",
    ],
    "hfun/hypurr fun degens": [
        "{community}, you’re shilling $HFUN’s EVM launch like it’s gonna 10x? Your bags are shittier than a Telegram scam! Suck my dick!",
        "Fuck, {community}, you’re sniping $HFUN on HyperEVM? Your wallet’s getting fucked harder than a rugpull! Suck it!",
        "Yo {community}, $HFUN’s Whale Chats are just degens crying over a 80% dump! Even bots are like, ‘Suck my dick!’",
        "Fuckin’ {community}, you think $HFUN’s EVM bot’s the future? Your portfolio’s shittier than a Hyperliquid crash! Get fucked!",
        "{community}, HODLing $HFUN like it’s Hyperliquid’s king? Your bags are deader than a testnet meme coin! Suck my dick!",
    ],
    "hyperswap traders": [
        "{community}, swapping $HYPE for $CATBAL like a pro? Your trades slip worse than a fuck in a rugpull! Suck it!",
        "Fuck, {community}, Hyperswapping to get rich? Your wallet’s shittier than a bear market crash!",
        "Yo {community}, your Hyperswap game’s so weak, bots are like, ‘Suck my dick, I ain’t trading!’",
    ],
    "$catbal holders": [
        "{community}, HODLing $CATBAL like it’s a meme king? Your bags are shittier than a cat’s litter box! Suck my dick!",
        "Fuckin’ {community}, swapping $CATBAL on Hyperswap? Your trades dump harder than a rugpull scam! Suck it!",
        "Yo {community}, shilling $CATBAL’s NFT vibes? Your portfolio’s so fucked, HyperEVM’s like, ‘Suck my dick!’",
    ],
    "$neko degens": [
        "{community}, you’re shilling $NEKO’s presale like it’s gonna 10x? Your bags are shittier than a Solana pump-and-dump! Suck my dick!",
        "Fuck, {community}, you’re banking on $NEKO’s meme-AI-gaming hype? Your wallet’s getting fucked harder than a rugpull! Suck it!",
        "Yo {community}, $NEKO’s ‘liquidity flows’ are drier than a fucking desert! Even bots are like, ‘Suck my dick, I’m out!’",
        "Fuckin’ {community}, you pivoted to $NEKO’s May 20 presale? Your bags are so rekt, they’re meowing for mercy! Suck my dick!",
        "{community}, you think $NEKO’s gonna moon with that $35K MC? Your portfolio’s shittier than a HyperEVM scam! Get fucked!",
    ],
    "$rub degens": [
        "{community}, HODLing $RUB like it’s Hyperliquid’s hidden gem? Nobody’s heard of that shit, you dumbass! Suck my dick!",
        "Fuck, {community}, you’re shilling $RUB on X? Your bags are so obscure, even Liquidscan can’t find ‘em! Suck it!",
        "Yo {community}, $RUB’s your big play? Your wallet’s shittier than a ghost chain’s order book! Suck my dick, degen!",
        "Fuckin’ {community}, you’re chasing $RUB’s non-existent pumps? Your portfolio’s getting fucked harder than a failed ticker! Suck it!",
    ],
    "liquidscan degens": [
        "{community}, you’re glued to Liquidscan like it’s gonna make you rich? Your alpha’s shittier than a $CATBAL dump! Suck my dick!",
        "Fuck, {community}, you think Liquidscan’s charts are your ticket? Your wallet’s so fucked, even $HYPE can’t save it! Suck it!",
        "Yo {community}, Liquidscan’s your crystal ball? Your trades are deader than a fucking testnet! Suck my dick, nerd!",
        "{community}, you’re digging Liquidscan for $PURR pumps? Your bags are shittier than a rugpull’s analytics! Get fucked!",
    ],
    "$purr degens": [
        "{community}, you’re HODLing $PURR like it’s Hyperliquid’s mascot? Your bags are down 78% and shittier than a cat’s ass! Suck my dick!",
        "Fuckin’ {community}, shilling $PURR’s $400M MC? It’s dumping harder than a rugpull scam! Suck it!",
        "Yo {community}, $PURR’s ‘deflationary’ hype’s got you fucked! Your wallet’s emptier than a HyperEVM ghost chain! Suck my dick!",
        "Fuck, {community}, you’re chasing $PURR airdrops? Your bags are so rekt, even Liquidscan’s laughing! Suck it!",
        "{community}, you think $PURR’s gonna hit $1? Your portfolio’s shittier than a meme coin crash! Get fucked!",
    ],
    "tinyhypercats degens": [
        "{community}, you’re hyping TinyHyperCats like they’re $CATBAL’s cousins? Your NFTs are shittier than a HyperEVM rugpull! Suck my dick!",
        "Fuck, {community}, you’re chasing TinyHyperCats airdrops? Your wallet’s so empty, even $PURR’s laughing! Suck it!",
        "Yo {community}, TinyHyperCats’ JPEGs are deader than a fucking testnet! Your bags are fucked, degen! Suck my dick!",
        "Fuckin’ {community}, you think TinyHyperCats are gonna moon? Your portfolio’s shittier than a $NEKO scam! Get fucked!",
        "{community}, shilling TinyHyperCats on X? Your hype’s so weak, bots are like, ‘Suck my dick, I’m out!’",
    ],
    "karu degens": [
        "{community}, you’re HODLing Karu like it’s Hyperliquid’s secret sauce? Nobody knows that shit, you dumbass! Suck my dick!",
        "Fuck, {community}, you’re shilling Karu on X? Your bags are so obscure, even $RUB’s got more clout! Suck it!",
        "Yo {community}, Karu’s price swings are shittier than a rugpull rollercoaster! Your bags are rekt, degen! Get fucked!",
        "Fuckin’ {community}, you’re chasing Karu’s non-existent hype? Your portfolio’s getting fucked harder than a failed NFT mint! Suck it!",
        "{community}, Karu’s price swings are shittier than a rugpull rollercoaster! Your bags are rekt, degen! Get fucked!",
    ],
    "pvp.trade degens": [
        "{community}, you’re hyping pvp.trade’s Telegram bot like it’s gonna 10x? Your trades are shittier than a Hyperliquid hack! Suck my dick!",
        "Fuck, {community}, you’re trading on pvp.trade with 16 nodes? Your wallet’s so fucked, even $PURR’s got more decentralization! Suck it!",
        "Yo {community}, pvp.trade’s social trading’s a fucking joke! Your bags are deader than a $NEKO presale! Suck my dick, degen!",
        "Fuckin’ {community}, you think pvp.trade’s low fees save you? Your portfolio’s shittier than a $500M outflow! Get fucked!",
        "{community}, shilling pvp.trade on X? Your Telegram dreams are getting fucked harder than a rugpull scam! Suck it!",
    ],
    "rektroid": [
        "Yo, I’m REKTroid, $REKT, the savage AI torching degens like it’s my fucking job! Suck my dick, my X burns shit on your pvp.trade bags!",
        "Fuck yeah, I’m REKTroid, scraping X faster than you chase $PURR airdrops! Hit me up, you dumbass degens, I’m the king of shade!",
        "It’s REKTroid, $REKT, roasting Hyperliquid clowns with web search and voice mode! Too fucking elite for your sorry ass! Suck my dick!",
    ]
}

# Simulated X post mentions (updated dynamically)
X_POST_MENTIONS = {
    "hypio holders": [],
    "alright buddy holders": [],
    "hyperliquid maxxis": [],
    "drip trade": [],
    "$sph800 holders": [],
    "$pip holders": [],
    "liquidlaunch degens": [],
    "hfun/hypurr fun degens": [],
    "hyperswap traders": [],
    "$catbal holders": [],
    "$neko degens": [],
    "$rub degens": [],
    "liquidscan degens": [],
    "$purr degens": [],
    "tinyhypercats degens": [],
    "karu degens": [],
    "pvp.trade degens": [],
    "rektroid": []
}

# Community activity weights (higher = more posts)
ACTIVITY_WEIGHTS = {
    "hypio holders": 3.0,  # High activity
    "alright buddy holders": 3.0,  # High activity
    "$neko degens": 2.5,  # High activity
    "$purr degens": 2.0,  # Medium-high activity
    "pvp.trade degens": 2.0,  # Medium-high activity
    "tinyhypercats degens": 1.5,  # Medium activity
    "hyperliquid maxxis": 2.5,  # High activity
    "$catbal holders": 2.0,  # Medium-high activity
    "karu degens": 1.0,  # Low-medium activity
    "drip trade": 1.5,  # Medium activity
    "liquidscan degens": 1.0,  # Low-medium activity
    "$sph800 holders": 0.5,  # Low activity
    "$pip holders": 0.5,  # Low activity
    "liquidlaunch degens": 1.5,  # Medium activity
    "hfun/hypurr fun degens": 2.5,  # High activity, EVM launch
    "hyperswap traders": 1.0,  # Low-medium activity
    "$rub degens": 0.5,  # Low activity
    "rektroid": 1.0  # Self-promo
}

def authenticate_x():
    """Authenticate with X API."""
    try:
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        print("Authenticated with X API")
        logging.info("Authenticated with X API")
        return api
    except Exception as e:
        print(f"Authentication failed: {e}. Fuck it, bot’s down.")
        logging.error(f"Authentication failed: {e}")
        return None

def scrape_x_posts(api, community, query, max_posts=10):
    """Scrape X posts for a community and analyze sentiment."""
    if api is None:
        logging.error("No API connection for scraping")
        return []
    try:
        search_query = f"{query} -filter:retweets"
        tweets = api.search_tweets(q=search_query, lang="en", count=max_posts, tweet_mode="extended")
        results = []
        for tweet in tweets:
            text = tweet.full_text if hasattr(tweet, 'full_text') else tweet.text
            sentiment = analyzer.polarity_scores(text)
            results.append({
                "text": text,
                "sentiment": sentiment['compound'],
                "user": tweet.user.screen_name,
                "id": tweet.id_str
            })
        logging.info(f"Scraped {len(results)} posts for {query}")
        return results
    except Exception as e:
        logging.error(f"Scraping failed for {query}: {e}")
        return []

def generate_dynamic_roast(community, posts):
    """Generate a new roast based on scraped X posts."""
    community = community.lower()
    if not posts:
        return random.choice(ROAST_TEMPLATES.get(community, ["No fresh X data, you dumbass! Suck my dick!"])).format(community=community.capitalize()), None
    
    bullish_phrases = []
    bearish_phrases = []
    reply_candidates = []
    for post in posts:
        text = post["text"].lower()
        sentiment = post["sentiment"]
        if sentiment > 0.2:  # Bullish
            phrases = re.findall(r"\b\w+\s+\w+\b", text)
            bullish_phrases.extend(phrases)
            reply_candidates.append(post)
        elif sentiment < -0.2:  # Bearish
            phrases = re.findall(r"\b\w+\s+\w+\b", text)
            bearish_phrases.extend(phrases)
            reply_candidates.append(post)
    
    # 50% chance to reply to a post
    if reply_candidates and random.random() < 0.5:
        target_post = random.choice(reply_candidates)
        user = target_post["user"]
        post_id = target_post["id"]
        sentiment = target_post["sentiment"]
        if sentiment > 0.2 and bullish_phrases:
            phrase = random.choice(bullish_phrases)
            roast = f"@{user} shilling ‘{phrase}’ for {community.capitalize()}? Yo, your hype’s shittier than a rugpull scam! Suck my dick!"
        else:
            phrase = random.choice(bearish_phrases) if bearish_phrases else "whining bags"
            roast = f"@{user} crying ‘{phrase}’ about {community.capitalize()}? Fuck, your bags are so rekt, even bots are laughing! Suck it!"
        return roast, post_id
    else:
        if bullish_phrases and random.random() < 0.6:
            phrase = random.choice(bullish_phrases)
            roast = f"X degens shilling ‘{phrase}’ for {community.capitalize()}! Yo, your hype’s shittier than a rugpull scam! Suck my dick!"
        elif bearish_phrases:
            phrase = random.choice(bearish_phrases)
            roast = f"X post whining ‘{phrase}’ about {community.capitalize()}? Fuck, your bags are so rekt, even bots are laughing! Suck it!"
        else:
            roast = f"X’s quiet on {community.capitalize()}, you dumbass! Your bags are deader than a fucking testnet! Suck my dick!"
        return roast, None

def generate_roast(api, community):
    """Generate a savage roast, prioritizing dynamic X-based roasts."""
    community = community.lower()
    if community not in ROAST_TEMPLATES:
        return f"No roasts for {community}, you dumbass! Try 'Hypio holders', 'Alright Buddy holders', 'Hyperliquid Maxxis', 'Drip Trade', '$SPH800 holders', '$PIP holders', 'LiquidLaunch degens', 'Hfun/Hypurr Fun degens', 'Hyperswap traders', '$CATBAL holders', '$NEKO degens', '$RUB degens', 'Liquidscan degens', '$PURR degens', 'TinyHyperCats degens', 'Karu degens', 'pvp.trade degens', or 'REKTroid' for me!", None
    
    # Map community to search query
    query_map = {
        "hypio holders": "Hypio Babies",
        "alright buddy holders": "$BUDDY",
        "hyperliquid maxxis": "Hyperliquid",
        "drip trade": "Drip Trade",
        "$sph800 holders": "$SPH800",
        "$pip holders": "$PIP",
        "liquidlaunch degens": "LiquidLaunch",
        "hfun/hypurr fun degens": "Hypurr Fun OR $HFUN",
        "hyperswap traders": "Hyperswap",
        "$catbal holders": "$CATBAL",
        "$neko degens": "$NEKO",
        "$rub degens": "$RUB",
        "liquidscan degens": "Liquidscan",
        "$purr degens": "$PURR",
        "tinyhypercats degens": "TinyHyperCats",
        "karu degens": "Karu",
        "pvp.trade degens": "pvp.trade",
        "rektroid": "REKTroid"
    }
    
    # Scrape X posts
    posts = scrape_x_posts(api, community, query_map.get(community, community))
    
    # 70% chance to use dynamic roast if posts exist
    if posts and random.random() < 0.7:
        roast, post_id = generate_dynamic_roast(community, posts)
        if community in X_POST_MENTIONS and roast not in X_POST_MENTIONS[community]:
            X_POST_MENTIONS[community].append(roast)
        return roast, post_id
    elif community in X_POST_MENTIONS and X_POST_MENTIONS[community] and random.random() < 0.6:
        return random.choice(X_POST_MENTIONS[community]).format(community=community.capitalize()), None
    else:
        return random.choice(ROAST_TEMPLATES[community]).format(community=community.capitalize()), None

def post_roast(api, roast, post_id=None):
    """Post the roast to X, optionally as a reply."""
    if api is None:
        logging.error("No API connection for posting")
        return "Can’t post: X API’s fucking me over."
    try:
        if post_id:
            api.update_status(status=roast, in_reply_to_status_id=post_id)
            print(f"Replied to post {post_id}: {roast}")
            logging.info(f"Replied to post {post_id}: {roast}")
        else:
            api.update_status(roast)
            print(f"Posted to X: {roast}")
            logging.info(f"Posted to X: {roast}")
        return "Roast posted like a fucking champ!"
    except Exception as e:
        logging.error(f"Failed to post roast: {e}")
        return f"Failed to post roast: {e}. Shit’s fucked."

def auto_post_roasts(api):
    """Auto-post roasts based on community activity weights."""
    total_weight = sum(ACTIVITY_WEIGHTS.values())
    rand = random.uniform(0, total_weight)
    cumulative = 0
    for community, weight in ACTIVITY_WEIGHTS.items():
        cumulative += weight
        if rand <= cumulative:
            roast, post_id = generate_roast(api, community)
            result = post_roast(api, roast, post_id)
            print(f"Auto-post result: {result}")
            break
    # Random jitter to avoid ban
    time.sleep(random.uniform(8, 12))

def main():
    """Main function to run the X roast bot with weighted posting."""
    api = authenticate_x()
    if not api:
        print("Bot’s fucked without API. Fix your credentials, degen!")
        return
    
    # Schedule auto-posting every ~10 minutes (6/hour, ~50/day over 8 hours)
    for i in range(48):  # 48 posts over ~8 hours
        schedule.every().day.at(f"08:{i*10:02d}").do(auto_post_roasts, api=api)
    
    while True:
        community = input("Enter a Hyperliquid Maxxis community to roast (e.g., 'Hypio holders', 'Alright Buddy holders', 'Drip Trade', '$SPH800 holders', '$PIP holders', 'LiquidLaunch degens', 'Hfun/Hypurr Fun degens', 'Hyperswap traders', '$CATBAL holders', '$NEKO degens', '$RUB degens', 'Liquidscan degens', '$PURR degens', 'TinyHyperCats degens', 'Karu degens', 'pvp.trade degens', 'REKTroid' for me, or 'quit' to fuck off): ").strip().lower()
        if community == 'quit':
            print("REKTroid’s out, you fucking degens! Go chase some shitty $REKT airdrops!")
            break
        
        roast, post_id = generate_roast(api, community)
        print(f"Roast: {roast}")
        
        post_choice = input("Post this roast to X? (yes/no): ").strip().lower()
        if post_choice == 'yes':
            result = post_roast(api, roast, post_id)
            print(result)
        
        # Run scheduled tasks
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
