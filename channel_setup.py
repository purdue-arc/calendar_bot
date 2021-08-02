import discord
import json

client = discord.Client()
discord_config = json.load(open('discord_config.json', 'r'))

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$remindhere'):
        if "high council" in [r.name.lower() for r in message.author.roles]:
            discord_config['channels'].append(message.channel.name)
            json.dump(discord_config, open('discord_config.json', 'w'))
            await message.channel.send('Sending reminders in this channel.')

@client.event
async def on_disconnect():
    json.dump(discord_config, open('discord_config.json', 'w'))

client.run(discord_config['token'])