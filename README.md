**Calendar Bot** relays upcoming Google Calendar events.

[![Discord](https://img.shields.io/discord/868977679590883420)](https://discord.gg/xPJfDaztvS)

## Setup

Add app to Heroku, then configure scheduled run of the following command:

```bash
python send_updates.py
```

The set schedule helps parametrize when updates are sent to discord.

`send_updates.py` is currently written to obtain daily events, so the command should be scheduled to run daily.

This application relies on four environment variables:

- `GOOGLE_SERVICE_ACCOUNT_JSON`: json string given by Google API service account
- `CALENDAR_ID`: ID for respective Google Calendar
- `DISCORD_TOKEN`: bot token given by Discord
- `REDIS_URL`: URL for Redis file store (provided by Redis Heroku application)

## Usage

After adding Discord bot to a server and deploying on Heroku, simply choose a text channel and send the command:

```
.remindhere
```

If working, the bot should reply with:

```
Sending reminders in this channel.
```

Calendar updates will be delivered on each run of `send_updates.py`.
