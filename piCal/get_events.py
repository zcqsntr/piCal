from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json



def get_events(calender_ids):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            print('hello', creds and creds.expired and creds.refresh_token)
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())



    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        all_es = []
        for calender_id in calender_ids:
            events_result = service.events().list(calendarId=calender_id, timeMin=now,
                                                  maxResults=1000, singleEvents=True,
                                                  orderBy='startTime').execute()

            events = events_result.get('items', [])

            # Prints the start and name of the next 10 events
            es = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                es.append({'start':event['start'].get('dateTime', event['start'].get('date')), 'end':event['end'].get('dateTime', event['end'].get('date')), 'name':event['summary']})
                print('from', start, 'to',  end,  event['summary'])
            all_es.append(es)

        return all_es

    except HttpError as error:
        print('An error occurred: %s' % error)
        return [[None], [None]]


if __name__ == '__main__':
    # If modifying these scopes, delete the file token.json.
    

    calendar_ids = ['6e56207b41dd787f37a38aa0794de8dab5243c611088ca04ad54ac9c478abbdb@group.calendar.google.com', 'en.uk#holiday@group.v.calendar.google.com']
    events, holidays = get_events(calendar_ids)

    json.dump(holidays, open('data/holidays.json', 'w+'))
    json.dump(events, open('data/events.json', 'w+'))
