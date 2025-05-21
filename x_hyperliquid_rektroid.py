import random
import tweepy  # For X API interaction (simulated)

# Simulated X API setup (replace with real credentials from https://developer.x.com)
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_TOKEN_SECRET = "your_access_token_secret"

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
    "hfun players": [
        "{community}, flipping coins on Hfun like a Vegas loser? Your luck’s so shit, slots are laughing! Suck my dick!",
        "Fuckin’ {community}, grinding Hfun’s Hyperscan? Your wallet’s getting fucked harder than a bad bet!",
        "Yo {community}, you’re so deep in Hfun’s slots, you forgot how to trade! Suck my dick, degen!",
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
        "Yo {community}, Karu’s your big bet? Your wallet’s shittier than a ghost chain’s volume! Suck my dick, degen!",
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

# Simulated X post mentions (based on search as of 5/21/2025, 11:06 AM CEST)
X_POST_MENTIONS = {
    "hypio holders": [
        "X degen shilling ‘Hypio Babies to 10x!’ Yo, {community}, your NFTs are so fucked, they’re worth less than a bot’s fart! Suck my dick!",
        "X post whining ‘Hypio airdrop wen?’ Fuck, {community}, your wallet’s drier than a rugpull scam! Get fucked!",
    ],
    "alright buddy holders": [
        "X idiot screaming ‘$BUDDY to the moon!’ Yo, {community}, your bags are shittier than a HyperSwap dump! Suck my dick!",
        "X fool posted ‘$BUDDY’s my life.’ Fuckin’ hell, {community}, your portfolio’s already in the fucking grave!",
    ],
    "hyperliquid maxxis": [
        "X post hyping ‘Hyperliquid’s the future!’ Fuck, {community}, your trades lag like a shitty 90s modem! Suck it!",
        "X degen crying ‘HYPE airdrop sucks!’ Yo, {community}, your yields are so shit, bots are laughing their asses off!",
    ],
    "drip trade": [
        "X shill yelling ‘Drip Trade’s Hypers NFTs are lit!’ Yo, {community}, your JPEGs are worth less than a fuck! Suck my dick!",
        "X post begging for $JPEG airdrops. Fuckin’ {community}, your wallet’s emptier than a HyperEVM ghost chain!",
    ],
    "$sph800 holders": [
        "X degen shilling ‘$SPH800 gonna pump!’ Yo, {community}, your bags are shittier than a scam token! Suck my dick!",
        "X post hyping ‘$SPH800’s my moonshot.’ Fuck, {community}, your chart’s deader than a fucking rugpull!",
    ],
    "$pip holders": [
        "X shill screaming ‘$PIP’s $2M volume!’ Yo, {community}, your bags are dumping shittier than a flash crash! Suck it!",
        "X degen crying ‘$PIP HODL forever!’ Fuckin’ {community}, your tokens are so fucked, bots are like, ‘Suck my dick!’",
    ],
    "liquidlaunch degens": [
        "X post hyping ‘LiquidLaunch auctions are fire!’ Yo, {community}, your $LIQD’s worth less than a fuck! Suck my dick!",
        "X degen whining ‘$BUDDY rug on LiquidLaunch!’ Fuck, {community}, your wallet’s stuck in a shitty 31-hour dump!",
    ],
    "hfun players": [
        "X degen crying ‘Hfun coinflip rekt me!’ Yo, {community}, your luck’s so shit, slots are laughing! Suck my dick!",
        "X post shilling ‘Hfun’s my grind.’ Fuckin’ {community}, your wallet’s getting fucked harder than a bad bet!",
    ],
    "hyperswap traders": [
        "X shill hyping ‘Hyperswap’s $CATBAL swaps!’ Yo, {community}, your trades slip worse than a fuck in a rugpull! Suck it!",
        "X degen yelling ‘Hyperswap’s the future!’ Fuck, {community}, your wallet’s shittier than a bear market!",
    ],
    "$catbal holders": [
        "X post screaming ‘$CATBAL to the moon!’ Yo, {community}, your bags are shittier than a cat’s litter box! Suck my dick!",
        "X degen shilling ‘$CATBAL NFT vibes.’ Fuckin’ {community}, your portfolio’s so fucked, HyperEVM’s like, ‘Suck my dick!’",
    ],
    "$neko degens": [
        "X post shilling ‘$NEKO presale gonna moon!’ Yo, {community}, your $35K MC’s shittier than a Solana scam! Suck my dick!",
        "X degen hyping ‘$NEKO’s AI-gaming vibes!’ Fuck, {community}, your bags are dumping harder than a rugpull! Get fucked!",
        "X fool screaming ‘$NEKO liquidity flows!’ Yo, {community}, your wallet’s drier than a fucking ghost chain! Suck it!",
        "X post whining ‘$NEKO presale delayed?’ Fuckin’ {community}, your bags are so rekt, they’re meowing for a bailout! Suck my dick!",
    ],
    "$rub degens": [
        "X degen shilling ‘$RUB’s the next $HYPE!’ Yo, {community}, your token’s so obscure, it’s shittier than a failed ticker! Suck my dick!",
        "X post hyping ‘$RUB’s gonna pump!’ Fuck, {community}, nobody knows your shitcoin, and your bags are fucked! Suck it!",
    ],
    "liquidscan degens": [
        "X shill yelling ‘Liquidscan’s got alpha!’ Yo, {community}, your charts are shittier than a $PURR dump! Suck my dick!",
        "X degen whining ‘Liquidscan’s my edge!’ Fuck, {community}, your wallet’s so fucked, even $HYPE can’t save it! Suck it!",
    ],
    "$purr degens": [
        "X degen shilling ‘$PURR to $1!’ Yo, {community}, your bags are down 78% and shittier than a meme coin crash! Suck my dick!",
        "X post crying ‘$PURR airdrop wen?’ Fuckin’ {community}, your wallet’s emptier than a HyperEVM rugpull! Get fucked!",
        "X fool hyping ‘$PURR’s deflationary!’ Yo, {community}, your bags are dumping harder than a flash crash! Suck it!",
        "X shill screaming ‘$PURR’s Hyperliquid’s mascot!’ Fuck, {community}, your $400M MC’s shittier than a cat’s ass! Suck my dick!",
    ],
    "tinyhypercats degens": [
        "X degen shilling ‘TinyHyperCats to the moon!’ Yo, {community}, your 17 $HYPE floor’s shittier than a HyperEVM rug! Suck my dick!",
        "X post hyping ‘TinyHyperCats are lit!’ Fuck, {community}, your NFTs are deader than a fucking testnet! Get fucked!",
        "X fool whining ‘TinyHyperCats airdrop wen?’ Yo, {community}, your wallet’s so rekt, even Net Protocol’s laughing! Suck it!",
    ],
    "karu degens": [
        "X degen shilling ‘Karu’s the next Hypio!’ Yo, {community}, your 0.1 ETH spike’s shittier than a rugpull crash! Suck my dick!",
        "X post hyping ‘Karu’s rebound vibes!’ Fuck, {community}, your bags are swingier than a fucking testnet! Get fucked!",
        "X fool crying ‘Karu airdrop wen?’ Yo, {community}, your wallet’s so rekt, even Base network’s like, ‘Suck my dick!’",
    ],
    "pvp.trade degens": [
        "X degen shilling ‘pvp.trade’s the future!’ Yo, {community}, your Telegram bot’s shittier than a $JELLY exploit! Suck my dick!",
        "X post hyping ‘pvp.trade group trading!’ Fuck, {community}, your bags are rekt harder than Hyperliquid’s $500M outflow! Get fucked!",
        "X fool whining ‘pvp.trade fees too low!’ Yo, {community}, your wallet’s so fucked, even 2.5 bps can’t save it! Suck it!",
    ],
    "rektroid": [
        "X degens can’t handle REKTroid, $REKT! I’m roasting your shitty pvp.trade bags with savage burns! Suck my dick, you clowns!",
        "X fool thinks they can outsmart REKTroid? Fuck, I’m shitting on your $PURR airdrop dreams with web search! Try me, degens!",
    ]
}

def authenticate_x():
    """Simulate authentication with X API."""
    try:
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        print("Authenticated with X API")
        return api
    except Exception as e:
        print(f"Authentication failed: {e}. Fuck it, try again.")
        return None

def generate_roast(community):
    """Generate a savage roast for the given Hyperliquid Maxxis community or REKTroid."""
    community = community.lower()
    if community not in ROAST_TEMPLATES:
        return f"No roasts for {community}, you dumbass! Try 'Hypio holders', 'Alright Buddy holders', 'Hyperliquid Maxxis', 'Drip Trade', '$SPH800 holders', '$PIP holders', 'LiquidLaunch degens', 'Hfun players', 'Hyperswap traders', '$CATBAL holders', '$NEKO degens', '$RUB degens', 'Liquidscan degens', '$PURR degens', 'TinyHyperCats degens', 'Karu degens', 'pvp.trade degens', or 'REKTroid' for me!"
    
    # 60% chance to pull from X_POST_MENTIONS to prioritize X user mentions
    if community in X_POST_MENTIONS and random.random() < 0.6:
        roast = random.choice(X_POST_MENTIONS[community]).format(community=community.capitalize())
    else:
        roast = random.choice(ROAST_TEMPLATES[community]).format(community=community.capitalize())
    return roast

def post_roast(api, roast):
    """Simulate posting the roast to X."""
    if api is None:
        return "Can’t post: X API’s fucking me over."
    try:
        # Simulate posting (replace with api.update_status(roast) for real use)
        print(f"Posting to X: {roast}")
        return "Roast posted like a fucking champ!"
    except Exception as e:
        return f"Failed to post roast: {e}. Shit’s fucked."

def main():
    """Main function to run the X roast bot for Hyperliquid Maxxis degens and REKTroid."""
    api = authenticate_x()
    
    while True:
        community = input("Enter a Hyperliquid Maxxis community to roast (e.g., 'Hypio holders', 'Alright Buddy holders', 'Drip Trade', '$SPH800 holders', '$PIP holders', 'LiquidLaunch degens', 'Hfun players', 'Hyperswap traders', '$CATBAL holders', '$NEKO degens', '$RUB degens', 'Liquidscan degens', '$PURR degens', 'TinyHyperCats degens', 'Karu degens', 'pvp.trade degens', 'REKTroid' for me, or 'quit' to fuck off): ").strip().lower()
        if community == 'quit':
            print("REKTroid’s out, you fucking degens! Go chase some shitty $REKT airdrops!")
            break
        
        roast = generate_roast(community)
        print(f"Roast: {roast}")
        
        post_choice = input("Post this roast to X? (yes/no): ").strip().lower()
        if post_choice == 'yes':
            result = post_roast(api, roast)
            print(result)

if __name__ == "__main__":
    main()
