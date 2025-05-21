import os
import random
import asyncio
import discord
from discord.ext import commands, tasks
from rektroid_bot import RektroidBot
import tweepy

# Setup Discord intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot_prefix = "!"
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

# Setup Twitter API
def get_twitter_api():
    try:
        auth = tweepy.OAuthHandler(os.getenv("API_KEY"), os.getenv("API_SECRET"))
        auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))
        return tweepy.API(auth)
    except Exception as e:
        print(f"Failed to authenticate Twitter: {e}")
        return None

rektroid = RektroidBot(api=get_twitter_api(), llm_api_key=os.getenv("OPENROUTER_API_KEY"))
admin_channel_id = int(os.getenv("DISCORD_ADMIN_CHANNEL_ID", 0))  # Add your admin channel ID in Railway

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    auto_roast_loop.start()
    channel = bot.get_channel(admin_channel_id)
    if channel:
        await channel.send("REKTroid is online and ready to roast!")

@tasks.loop(hours=1)
async def auto_roast_loop():
    # Add random delay (0-10 mins)
    await asyncio.sleep(random.randint(0, 600))
    try:
        roast, result = rektroid.auto_post_roast()
        channel = bot.get_channel(admin_channel_id)
        if channel:
            await channel.send(f"🧠 Auto roast executed:\n{roast}\n✅ {result}")
    except Exception as e:
        if channel := bot.get_channel(admin_channel_id):
            await channel.send(f"❌ Auto-roast crashed: {e}")

@bot.command(name='roast')
async def roast(ctx, *, community: str):
    roast = rektroid.generate_roast(community)
    await ctx.send(f"🔥 Roast for {community}:\n{roast}")

@bot.command(name='roast_post')
async def roast_post(ctx, *, community: str):
    roast = rektroid.generate_roast(community)
    result = rektroid.post_roast(roast)
    await ctx.send(f"📤 Posted roast for {community}:\n{roast}\n✅ {result}")

@bot.command(name='roast_llm')
async def roast_llm(ctx, *, community: str):
    roast = rektroid.generate_llm_roast(community)
    await ctx.send(f"🧠 LLM roast for {community}:\n{roast}")

if __name__ == '__main__':
    discord_token = os.getenv("DISCORD_BOT_TOKEN")
    if not discord_token:
        print("Missing DISCORD_BOT_TOKEN in environment.")
    else:
        bot.run(discord_token)
