from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SERVICE_ACCOUNT_FILE = 'service-account.json'
ARC_CALENDAR = '8mmp47biqieqhn39slnf6rmi8s@group.calendar.google.com'


def collect_today(n=5):
    """
    Gets n events within 24 hours of current time.
    """

    # Initialize service account credentials
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    start = datetime.datetime.utcnow()
    end = start + datetime.timedelta(1)
    events_result = service.events().list(calendarId=ARC_CALENDAR,
                                          timeMin=start.isoformat() + 'Z',
                                          timeMax=end.isoformat() + 'Z',
                                          maxResults=n, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events
