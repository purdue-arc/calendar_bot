import discord
import arccalendar
import json

client = discord.Client()
reminder_channels = []


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$remindhere'):
        if "high council" in [r.name.lower() for r in message.author.roles]:
            reminder_channels.append(message.channel)
            await message.channel.send('Sending reminders in this channel.')

client.run('your token here')
