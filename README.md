Simple bot to relay upcoming Google Calendar events.

## Setup
Add app to Heroku, then configure scheduled run of the following command:

```bash
python send_updates.py
```

The set schedule helps parametrize when updates are sent to discord. 

`send_updates.py` is currently written to obtain daily events, so the command should be scheduled to run daily.

This application relies on two environment variables:
- `GOOGLE_SERVICE_ACCOUNT_JSON`: json string given by Google API service account
- `DISCORD_TOKEN`: bot token given by Discord

## Usage

After adding Discord bot to a server and deploying on Heroku, simply choose a text channel and send the command:

```
$remindhere
```

If working, the bot should reply with:

```
Sending reminders in this channel.
```
