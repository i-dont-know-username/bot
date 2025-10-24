import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from flask import Flask
import threading
import os

# Flask app for Render (keeps the service "alive")
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running! 🚀"

def run_flask():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} is online!')
    # Set status: Online with custom activity
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.custom, name="Custom - Made By Awesome Dev")
    )
    # Sync slash commands globally (or use guild=discord.Object(id=YOUR_GUILD_ID) for testing)
    try:
        synced = await client.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync: {e}')

@client.tree.command(name='say', description='Say a message in a channel')
@app_commands.describe(string='The message to send', channel='Optional: Target channel (defaults to current)')
async def say(interaction: discord.Interaction, string: str, channel: discord.TextChannel = None):
    if channel is None:
        channel = interaction.channel
    # Ephemeral reply in emphasis (bold)
    await interaction.response.send_message("**Sent message**", ephemeral=True)
    # Send the string to the channel
    await channel.send(string)

# Run the bot
async def run_bot():
    token = os.environ['DISCORD_TOKEN']  # Env var on Render
    await client.start(token)

if __name__ == '__main__':
    # Run Flask in a thread (for Render's web requirement)
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    # Run bot in main thread
    asyncio.run(run_bot())
