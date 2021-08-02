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
        if message.channel.name not in r.get('DISCORD_CHANNELS') and \
            "high council" in [r.name.lower() for r in message.author.roles]:
            r.lpush('DISCORD_CHANNELS', message.channel.name)
            await message.channel.send('Sending reminders in this channel.')

if 'DISCORD_TOKEN' in os.environ:
    client.run(os.environ['DISCORD_TOKEN'])
else:
    sys.exit("DISCORD_TOKEN is not set.")