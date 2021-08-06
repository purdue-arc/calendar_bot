"""
Polls servers for new channels to send calendar events to.
"""

import sys
import os
import discord
import redis
import my_calendar
from send_updates import send_update
from keep_alive import keep_alive

ADMIN_ROLE = 'high council'

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
        author_permitted = ADMIN_ROLE in [
            role.name.lower() for role in message.author.roles]
        if not channel_exists and author_permitted:
            r.sadd('DISCORD_CHANNELS', message.channel.name)
            await message.channel.send('Sending reminders in this channel.')
    elif message.content.startswith('.getupdates'):
        author_permitted = ADMIN_ROLE in [
            role.name.lower() for role in message.author.roles]
        if author_permitted:
            await send_update(message.channel, my_calendar.collect_today())
    elif message.content.startswith('.getchannels'):
        active_channels = r.smembers('DISCORD_CHANNELS')
        author_permitted = ADMIN_ROLE in [
            role.name.lower() for role in message.author.roles]
        if author_permitted:
            await message.channel.send('Sending reminders in channels; ' + str(active_channels))   
    elif message.content.startswith('.clearchannels'):
        r.flushall()
        await message.channel.send('Cleared all channels.')


if 'DISCORD_TOKEN' in os.environ:
    keep_alive()
    client.run(os.environ['DISCORD_TOKEN'])
else:
    sys.exit("DISCORD_TOKEN is not set.")
