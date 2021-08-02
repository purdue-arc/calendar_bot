import sys
import datetime
import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account


def create_service():
    # Initialize service account credentials
    if 'GOOGLE_SERVICE_ACCOUNT_JSON' not in os.environ:
        sys.exit("GOOGLE_SERVICE_ACCOUNT_JSON is not set.")

    info = json.loads(os.environ['GOOGLE_SERVICE_ACCOUNT_JSON'])
    creds = service_account.Credentials.from_service_account_info(info)
    return build('calendar', 'v3', credentials=creds)


def collect_today(n=5):
    """
    Gets n events within 24 hours of current time.
    """
    print("Parsing date")
    start = datetime.datetime.utcnow()
    end = start + datetime.timedelta(1)

    print("Checking calendar ID")
    if 'CALENDAR_ID' not in os.environ:
        sys.exit("CALENDAR_ID is not set.")

    print("Obtaining and returing events")
    calendarId = os.environ['CALENDAR_ID']
    events_result = create_service().events().list(calendarId=calendarId,
                                                   timeMin=start.isoformat() + 'Z',
                                                   timeMax=end.isoformat() + 'Z',
                                                   maxResults=n, singleEvents=True,
                                                   orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events


def collect_week(n=25):
    """
    Collects n google calendar events within a week of current time.
    """
    print("Parsing date")
    start = datetime.datetime.utcnow()
    end = start + datetime.timedelta(week=1)

    print("Checking calendar ID")
    if 'CALENDAR_ID' not in os.environ:
        sys.exit("CALENDAR_ID is not set.")

    calendarId = os.environ['CALENDAR_ID']

    print("Obtaining and returing events")
    events_result = create_service().events().list(calendarId=calendarId,
                                                   timeMin=start.isoformat() + 'Z',
                                                   timeMax=end.isoformat() + 'Z',
                                                   maxResults=n, singleEvents=True,
                                                   orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events
