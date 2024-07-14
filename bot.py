import discord
from discord.ext import commands
from utils import get_response_from_api
from initializing_variables import DISCORD_BOT_TOKEN


## intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True 


api_url = "http://127.0.0.1:8000/generate_response"
# Initialize the bot with a command prefix
bot = commands.Bot(command_prefix="/",  intents=intents)

# Define the tutor command
@bot.command(name="tutor")
async def tutor(ctx, *, prompt: str):
    # Call the API and get the response
    response = get_response_from_api(api_url, prompt)["response"]
    await ctx.send(response)

# Event handler for when the bot has logged in
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Replace 'YOUR_DISCORD_BOT_TOKEN' with your actual Discord bot token
bot.run(DISCORD_BOT_TOKEN)
