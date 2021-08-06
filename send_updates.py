"""
Grabs list of upcoming events, creates embed message and posts to discord.
"""

from datetime import datetime
import os
import sys
import discord
import redis
import my_calendar

TIMEZONE_LEN = 6

client = discord.Client()
r = redis.from_url(os.environ.get('REDIS_URL'))
active_channels = r.smembers('DISCORD_CHANNELS')


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
        start_date = datetime.strptime(
            calendar_event['start']['date'],
            '%Y-%m-%d'
        )
        end_date = datetime.strptime(
            calendar_event['end']['date'],
            '%Y-%m-%d'
        )

        # List first day
        date_msg = datetime.strftime(
            start_date, "%b %d "
        )

        # If event lasts more than one day, state range
        if start_date.date() != end_date.date():
            date_msg += datetime.strftime(
                end_date, "to %b %d"
            )
    else:
        # Convert date strings to datetime objects
        start_datetime = datetime.strptime(
            calendar_event['start']['dateTime'][:-TIMEZONE_LEN],
            '%Y-%m-%dT%H:%M:%S'
        )
        end_datetime = datetime.strptime(
            calendar_event['end']['dateTime'][:-TIMEZONE_LEN],
            '%Y-%m-%dT%H:%M:%S'
        )

        # List first day
        date_msg = datetime.strftime(
            start_datetime, "%b %d from %I:%M %p "
        )

        # If event lasts more than one day, append date end-point
        if start_datetime.date() != end_datetime.date():
            date_msg += datetime.strftime(
                end_datetime, "to %b %d %I:%M %p"
            )
        else:
            date_msg += datetime.strftime(
                end_datetime, "to %I:%M %p"
            )

    # Create embedded message
    msg = discord.Embed()
    msg.description = '[{name}]({event_url})\n {date_msg}'.format(
        name=calendar_event['summary'],
        event_url=calendar_event['htmlLink'],
        date_msg=date_msg
    )
    return msg


async def send_update(channel, calendar_events):
    if not calendar_events:
        # Commented out to reduce spam
        # await text_channel.send(
        #     content="No calendar events today."
        # )
        pass
    else:
        print("Sending events to {}".format(channel.name))
        for calendar_event in calendar_events:
            await channel.send(
                embed=construct_calendar_msg(calendar_event)
            )


@client.event
async def on_ready():
    """Finds active channels and sends out calendar event message"""
    print("Running calendar update")
    calendar_events = my_calendar.collect_today()
    for guild in client.guilds:
        for text_channel in guild.text_channels:
            name_bytes = text_channel.name.encode('UTF-8')
            if active_channels is not None and name_bytes in active_channels:
                print("Collecting events for {}".format(text_channel.name))
                await send_update(text_channel, calendar_events)
    print("Calendar update finished")
    await client.close()


if __name__ == "__main__":
    if 'DISCORD_TOKEN' in os.environ:
        client.run(os.environ['DISCORD_TOKEN'])
    else:
        sys.exit("DISCORD_TOKEN is not set.")
