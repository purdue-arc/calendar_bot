import discord
import os
import redis
import sys
import json

client = discord.Client()
r = redis.from_url(os.environ.get("REDIS_URL"))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$remindhere'):
        active_channels = r.smembers('DISCORD_CHANNELS')
        channel_exists = active_channels and message.channel.name not in active_channels
        author_permitted = 'high council' in [
            r.name.lower() for r in message.author.roles]
        if not channel_exists and author_permitted:
            r.sadd('DISCORD_CHANNELS', message.channel.name)
            await message.channel.send('Sending reminders in this channel.')

if 'DISCORD_TOKEN' in os.environ:
    client.run(os.environ['DISCORD_TOKEN'])
else:
    sys.exit("DISCORD_TOKEN is not set.")
