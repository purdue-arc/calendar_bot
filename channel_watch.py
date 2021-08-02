import discord
import os
import sys
import json

client = discord.Client()
if 'DISCORD_CHANNELS' in os.environ:
    active_channels = json.loads(os.environ['DISCORD_CHANNELS'])
else:
    print("DISCORD_CHANNELS not set, using empty list.")
    active_channels = []

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$remindhere'):
        if "high council" in [r.name.lower() for r in message.author.roles]:
            active_channels.append(message.channel.name)
            os.environ['DISCORD_CHANNELS'] = json.dumps(active_channels)
            await message.channel.send('Sending reminders in this channel.')

@client.event
async def on_disconnect():
    os.environ['DISCORD_CHANNELS'] = json.dumps(active_channels)

if 'DISCORD_TOKEN' in os.environ:
    client.run(os.environ['DISCORD_TOKEN'])
else:
    sys.exit("DISCORD_TOKEN is not set.")