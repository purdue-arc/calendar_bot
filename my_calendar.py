import sys
import datetime
import os
import json
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2 import service_account


def collect_today(n=5):
    """
    Gets n events within 24 hours of current time.
    """

    # Initialize service account credentials
    if 'GOOGLE_SERVICE_ACCOUNT_JSON' not in os.environ:
        sys.exit("GOOGLE_SERVICE_ACCOUNT_JSON is not set.")

    info = json.load(os.environ['GOOGLE_SERVICE_ACCOUNT_JSON'])
    creds = service_account.Credentials.from_service_account_info(info)
    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    start = datetime.datetime.utcnow()
    end = start + datetime.timedelta(1)

    if 'CALENDAR_ID' not in os.environ:
        sys.exit("CALENDAR_ID is not set.")

    calendarId = os.environ('CALENDAR_ID')
    events_result = service.events().list(calendarId=calendarId,
                                          timeMin=start.isoformat() + 'Z',
                                          timeMax=end.isoformat() + 'Z',
                                          maxResults=n, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events