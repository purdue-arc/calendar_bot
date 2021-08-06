"""
Polls servers for new channels to send calendar events to.
"""

import sys
import os
import discord
import redis
from keep_alive import keep_alive

client = discord.Client()
r = redis.from_url(os.environ.get("REDIS_URL"))


@client.event
async def on_ready():
    """Logs when bot is ready to watch"""
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    """
    Waits for '.remindhere' and stores channel for event reminders.
    """
    if message.author == client.user:
        return

    if message.content.startswith('.remindhere'):
        active_channels = r.smembers('DISCORD_CHANNELS')
        channel_exists = active_channels and message.channel.name not in active_channels
        author_permitted = 'high council' in [
            r.name.lower() for r in message.author.roles]
        if not channel_exists and author_permitted:
            r.sadd('DISCORD_CHANNELS', message.channel.name)
            await message.channel.send('Sending reminders in this channel.')

if 'DISCORD_TOKEN' in os.environ:
    keep_alive()
    client.run(os.environ['DISCORD_TOKEN'])
else:
    sys.exit("DISCORD_TOKEN is not set.")
