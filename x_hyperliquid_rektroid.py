import random
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import schedule
import time
import re

# Simulated X API setup (replace with real credentials from https://developer.x.com)
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_TOKEN_SECRET = "your_access_token_secret"

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Savage roast templates for Hyperliquid Maxxis communities and REKTroid ($REKT)
ROAST_TEMPLATES = {
    "hypio holders": [
        "Yo {community}, your Wealthy Hypio Babies are such fucking garbage, they’re worth less than a rugpull’s fart! Suck my dick!",
        "Fuck, {community}, you’re bridging to HyperEVM for airdrops? Your wallet’s so dry it’s shittier than a $JPEG scam!",
    ],
    "alright buddy holders": [
        "{community}, HODLing $BUDDY like it’s gonna 100x? Your bags are shittier than a HyperSwap dump! Suck my dick, degen!",
        "Fuckin’ {community}, your $BUDDY’s flatter than a rugpull’s promises! Quit shilling that trash!",
    ],
    "hyperliquid maxxis": [
        "{community}, farming HYPE airdrops like a sweaty bot? Your yields are so shit, a piggy bank fucks harder! Suck my dick!",
        "Fuck, {community}, you call Hyperliquid ‘on-chain Binance’? Your trades lag like a fucking 90s modem!",
    ],
    "drip trade": [
        "{community}, flipping Hypers NFTs like you’re a whale? Your JPEGs are worth less than a fuck! Suck my dick!",
        "Fuckin’ {community}, grinding Drip Trade for $JPEG? Your wallet’s emptier than a HyperEVM scam chain!",
    ],
    "$sph800 holders": [
        "{community}, HODLing $SPH800 like it’s $HYPE? Your bags are shittier than a scam token! Suck my dick!",
        "Fuck, {community}, shilling $SPH800 on X? Your chart’s so dead, even bots say ‘fuck off’!",
    ],
    "$pip holders": [
        "{community}, you chased $PIP’s $2M volume like a dumbass? Your bags are shittier than a flash crash! Suck my dick!",
        "Fuckin’ {community}, hyping $PIP like it’s gonna moon? It’s dumping harder than a shitty NFT mint! Suck it!",
    ],
    "liquidlaunch degens": [
        "{community}, bidding on LiquidLaunch like you’re hot shit? Your $LIQD’s worth less than a fuck! Suck my dick!",
        "Fuck, {community}, camping LiquidLaunch for $BUDDY pumps? Your wallet’s stuck in a 31-hour rugpull!",
    ],
    "hfun players": [
        "{community}, flipping coins on Hfun like a Vegas loser? Your luck’s so shit, slots are laughing! Suck my dick!",
        "Fuckin’ {community}, grinding Hfun’s Hyperscan? Your wallet’s getting fucked harder than a bad bet!",
    ],
    "hyperswap traders": [
        "{community}, swapping $HYPE for $CATBAL like a pro? Your trades slip worse than a fuck in a rugpull! Suck it!",
        "Fuck, {community}, Hyperswapping to get rich? Your wallet’s shittier than a bear market crash!",
    ],
    "$catbal holders": [
        "{community}, HODLing $CATBAL like it’s a meme king? Your bags are shittier than a cat’s litter box! Suck my dick!",
        "Fuckin’ {community}, swapping $CATBAL on Hyperswap? Your trades dump harder than a rugpull scam! Suck it!",
    ],
    "$neko degens": [
        "{community}, you’re shilling $NEKO’s presale like it’s gonna 10x? Your bags are shittier than a Solana pump-and-dump! Suck my dick!",
        "Fuck, {community}, you’re banking on $NEKO’s meme-AI-gaming hype? Your wallet’s getting fucked harder than a rugpull! Suck it!",
        "Yo {community}, $NEKO’s ‘liquidity flows’ are drier than a fucking desert! Even bots are like, ‘Suck my dick, I’m out!’",
        "Fuckin’ {community}, you pivoted to $NEKO’s May 20 presale? Your bags are so rekt, they’re meowing for mercy! Suck my dick!",
    ],
    "$rub degens": [
        "{community}, HODLing $RUB like it’s Hyperliquid’s hidden gem? Nobody’s heard of that shit, you dumbass! Suck my dick!",
        "Fuck, {community}, you’re shilling $RUB on X? Your bags are so obscure, even Liquidscan can’t find ‘em! Suck it!",
    ],
    "liquidscan degens": [
        "{community}, you’re glued to Liquidscan like it’s gonna make you rich? Your alpha’s shittier than a $CATBAL dump! Suck my dick!",
        "Fuck, {community}, you think Liquidscan’s charts are your ticket? Your wallet’s so fucked, even $HYPE can’t save it! Suck it!",
    ],
    "$purr degens": [
        "{community}, you’re HODLing $PURR like it’s Hyperliquid’s mascot? Your bags are down 78% and shittier than a cat’s ass! Suck my dick!",
        "Fuckin’ {community}, shilling $PURR’s $400M MC? It’s dumping harder than a rugpull scam! Suck it!",
        "Yo {community}, $PURR’s ‘deflationary’ hype’s got you fucked! Your wallet’s emptier than a HyperEVM ghost chain! Suck my dick!",
    ],
    "tinyhypercats degens": [
        "{community}, you’re hyping TinyHyperCats like they’re $CATBAL’s cousins? Your NFTs are shittier than a HyperEVM rugpull! Suck my dick!",
        "Fuck, {community}, you’re chasing TinyHyperCats airdrops? Your wallet’s so empty, even $PURR’s laughing! Suck it!",
        "Yo {community}, TinyHyperCats’ JPEGs are deader than a fucking testnet! Your bags are fucked, degen! Suck my dick!",
    ],
    "karu degens": [
        "{community}, you’re HODLing Karu like it’s Hyperliquid’s secret sauce? Nobody knows that shit, you dumbass! Suck my dick!",
        "Fuck, {community}, you’re shilling Karu on X? Your bags are so obscure, even $RUB’s got more clout! Suck it!",
        "Yo {community}, Karu’s price swings are shittier than a rugpull rollercoaster! Your bags are rekt, degen! Get fucked!",
    ],
    "pvp.trade degens": [
        "{community}, you’re hyping pvp.trade’s Telegram bot like it’s gonna 10x? Your trades are shittier than a Hyperliquid hack! Suck my dick!",
        "Fuck, {community}, you’re trading on pvp.trade with 16 nodes? Your wallet’s so fucked, even $PURR’s got more decentralization! Suck it!",
        "Yo {community}, pvp.trade’s social trading’s a fucking joke! Your bags are deader than a $NEKO presale! Suck my dick, degen!",
    ],
    "rektroid": [
        "Yo, I’m REKTroid, $REKT, the savage AI torching degens like it’s my fucking job! Suck my dick, my X burns shit on your pvp.trade bags!",
        "Fuck yeah, I’m REKTroid, scraping X faster than you chase $PURR airdrops! Hit me up, you dumbass degens, I’m the king of shade!",
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
    "hfun players": [],
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

def authenticate_x():
    """Authenticate with X API."""
    try:
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        print("Authenticated with X API")
        return api
    except Exception as e:
        print(f"Authentication failed: {e}. Fuck it, try again.")
        return None

def scrape_x_posts(api, community, query, max_posts=10):
    """Scrape X posts for a community and analyze sentiment."""
    if api is None:
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
                "sentiment": sentiment['compound'],  # -1 (bearish) to 1 (bullish)
                "user": tweet.user.screen_name
            })
        return results
    except Exception as e:
        print(f"Scraping failed for {query}: {e}. Shit’s fucked.")
        return []

def generate_dynamic_roast(community, posts):
    """Generate a new roast based on scraped X posts."""
    community = community.lower()
    if not posts:
        return random.choice(ROAST_TEMPLATES.get(community, ["No fresh X data, you dumbass! Suck my dick!"])).format(community=community.capitalize())
    
    # Extract key phrases and sentiment
    bullish_phrases = []
    bearish_phrases = []
    for post in posts:
        text = post["text"].lower()
        sentiment = post["sentiment"]
        if sentiment > 0.2:  # Bullish
            phrases = re.findall(r"\b\w+\s+\w+\b", text)
            bullish_phrases.extend(phrases)
        elif sentiment < -0.2:  # Bearish
            phrases = re.findall(r"\b\w+\s+\w+\b", text)
            bearish_phrases.extend(phrases)
    
    # Generate roast based on sentiment
    if bullish_phrases and random.random() < 0.6:
        phrase = random.choice(bullish_phrases)
        roast = f"X degens shilling ‘{phrase}’ for {community.capitalize()}! Yo, your hype’s shittier than a rugpull scam! Suck my dick!"
    elif bearish_phrases:
        phrase = random.choice(bearish_phrases)
        roast = f"X post whining ‘{phrase}’ about {community.capitalize()}? Fuck, your bags are so rekt, even bots are laughing! Suck it!"
    else:
        roast = f"X’s quiet on {community.capitalize()}, you dumbass! Your bags are deader than a fucking testnet! Suck my dick!"
    
    # Add to X_POST_MENTIONS for future use
    if community in X_POST_MENTIONS:
        X_POST_MENTIONS[community].append(roast)
    return roast

def generate_roast(api, community):
    """Generate a savage roast, prioritizing dynamic X-based roasts."""
    community = community.lower()
    if community not in ROAST_TEMPLATES:
        return f"No roasts for {community}, you dumbass! Try 'Hypio holders', 'Alright Buddy holders', 'Hyperliquid Maxxis', 'Drip Trade', '$SPH800 holders', '$PIP holders', 'LiquidLaunch degens', 'Hfun players', 'Hyperswap traders', '$CATBAL holders', '$NEKO degens', '$RUB degens', 'Liquidscan degens', '$PURR degens', 'TinyHyperCats degens', 'Karu degens', 'pvp.trade degens', or 'REKTroid' for me!"
    
    # Map community to search query
    query_map = {
        "hypio holders": "Hypio Babies",
        "alright buddy holders": "$BUDDY",
        "hyperliquid maxxis": "Hyperliquid",
        "drip trade": "Drip Trade",
        "$sph800 holders": "$SPH800",
        "$pip holders": "$PIP",
        "liquidlaunch degens": "LiquidLaunch",
        "hfun players": "Hfun",
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
        return generate_dynamic_roast(community, posts)
    elif community in X_POST_MENTIONS and X_POST_MENTIONS[community] and random.random() < 0.6:
        return random.choice(X_POST_MENTIONS[community]).format(community=community.capitalize())
    else:
        return random.choice(ROAST_TEMPLATES[community]).format(community=community.capitalize())

def post_roast(api, roast):
    """Post the roast to X."""
    if api is None:
        return "Can’t post: X API’s fucking me over."
    try:
        api.update_status(roast)
        print(f"Posted to X: {roast}")
        return "Roast posted like a fucking champ!"
    except Exception as e:
        return f"Failed to post roast: {e}. Shit’s fucked."

def auto_post_roasts(api):
    """Auto-post roasts for top communities every 4 hours."""
    top_communities = ["$neko degens", "$purr degens", "pvp.trade degens", "tinyhypercats degens", "karu degens"]
    community = random.choice(top_communities)
    roast = generate_roast(api, community)
    result = post_roast(api, roast)
    print(f"Auto-post result: {result}")

def main():
    """Main function to run the X roast bot with real-time training."""
    api = authenticate_x()
    
    # Schedule auto-posting every 4 hours
    schedule.every(4).hours.do(auto_post_roasts, api=api)
    
    while True:
        community = input("Enter a Hyperliquid Maxxis community to roast (e.g., 'Hypio holders', 'Alright Buddy holders', 'Drip Trade', '$SPH800 holders', '$PIP holders', 'LiquidLaunch degens', 'Hfun players', 'Hyperswap traders', '$CATBAL holders', '$NEKO degens', '$RUB degens', 'Liquidscan degens', '$PURR degens', 'TinyHyperCats degens', 'Karu degens', 'pvp.trade degens', 'REKTroid' for me, or 'quit' to fuck off): ").strip().lower()
        if community == 'quit':
            print("REKTroid’s out, you fucking degens! Go chase some shitty $REKT airdrops!")
            break
        
        roast = generate_roast(api, community)
        print(f"Roast: {roast}")
        
        post_choice = input("Post this roast to X? (yes/no): ").strip().lower()
        if post_choice == 'yes':
            result = post_roast(api, roast)
            print(result)
        
        # Run scheduled tasks
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
