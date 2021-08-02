import discord
import arc_calendar
import json
from datetime import datetime

TIMEZONE_LEN = 6

client = discord.Client()
discord_config = json.load(open('discord-config.json', 'r'))

def construct_calendar_msg(calendar_event):
    """
    Transforms Google Calendar response to Discord-ready message.

    Format options (varies by response):
        - Event name\n Aug 02
        - Event name\n Aug 02 - Aug 03
        - Event name\n Aug 02 02:00 PM to 03:00 PM
        - Event name\n Aug 02 2:00 PM to Aug 03 3:00 PM

    Event name is embedded with Google Calendar link.
    """

    if 'date' in calendar_event['start']:
        # Convert date strings to datetime objects
        startDate = datetime.strptime(
            calendar_event['start']['date'],
            '%Y-%m-%d'
        )
        endDate = datetime.strptime(
            calendar_event['end']['date'],
            '%Y-%m-%d'
        )
        
        # List first day
        dateMsg = datetime.strftime(
            startDate, "%b %d "
        )

        # If event lasts more than one day, state range
        if startDate.date() != endDate.date():
            dateMsg += datetime.strftime(
                endDate, "to %b %d"
            )
    else:
        # Convert date strings to datetime objects
        startDateTime = datetime.strptime(
            calendar_event['start']['dateTime'][:-TIMEZONE_LEN],
            '%Y-%m-%dT%H:%M:%S'
        )
        endDateTime = datetime.strptime(
            calendar_event['end']['dateTime'][:-TIMEZONE_LEN],
            '%Y-%m-%dT%H:%M:%S'
        )
        
        # List first day
        dateMsg = datetime.strftime(
            startDateTime, "%b %d from %I:%M %p "
        )

        # If event lasts more than one day, append date end-point
        if startDateTime.date() != endDateTime.date():
            dateMsg += datetime.strftime(
                endDateTime, "to %b %d %I:%M %p"
            )
        else:
            dateMsg += datetime.strftime(
                endDateTime, "to %I:%M %p"
            )

    # Create embedded message
    msg = discord.Embed()
    msg.description = '[{name}]({event_url})\n {dateMsg}'.format(
        name=calendar_event['summary'],
        event_url=calendar_event['htmlLink'],
        dateMsg=dateMsg
    )
    return msg

@client.event
async def on_ready():
    for guild in client.guilds:
        for text_channel in guild.text_channels:
            if text_channel.name in discord_config['channels']:
                calendar_events = arc_calendar.collect_today(15)
                if not calendar_events:
                    await text_channel.send(
                        content="No calendar events today."
                    )
                else:
                    for calendar_event in calendar_events:
                        await text_channel.send(
                            embed=construct_calendar_msg(calendar_event)
                        )

client.run(discord_config['token'])