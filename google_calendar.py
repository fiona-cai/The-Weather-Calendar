"""Google Calendar API integration for managing weather events."""
import os
import pickle
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import Config

SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarManager:
    """Manages Google Calendar operations."""
    
    def __init__(self):
        self.service = None
        self.calendar_id = None
        self._authenticate()
        self._ensure_calendar_exists()
    
    def _authenticate(self):
        """Authenticate with Google Calendar API."""
        creds = None
        token_file = 'token.pickle'
        
        # Load existing token
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    raise FileNotFoundError(
                        "credentials.json not found. Please download it from Google Cloud Console."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=8080)
            
            # Save credentials for next run
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('calendar', 'v3', credentials=creds)
    
    def _ensure_calendar_exists(self):
        """Create the weather calendar if it doesn't exist."""
        try:
            # Search for existing calendar
            calendar_list = self.service.calendarList().list().execute()
            
            for calendar in calendar_list.get('items', []):
                if calendar['summary'] == Config.CALENDAR_NAME:
                    self.calendar_id = calendar['id']
                    return
            
            # Create new calendar if not found
            calendar_body = {
                'summary': Config.CALENDAR_NAME,
                'description': 'Automatically generated weather alerts and suggestions',
                'timeZone': 'America/New_York'
            }
            
            created_calendar = self.service.calendars().insert(body=calendar_body).execute()
            self.calendar_id = created_calendar['id']
            print(f"Created calendar: {Config.CALENDAR_NAME} (ID: {self.calendar_id})")
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            raise
    
    def create_event(self, title, description, start_time, end_time, location=None):
        """Create a new calendar event."""
        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'America/New_York',
            },
        }
        
        if location:
            event['location'] = location
        
        try:
            event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event
            ).execute()
            print(f"Created event: {title} at {start_time}")
            return event['id']
        except HttpError as error:
            print(f"An error occurred creating event: {error}")
            return None
    
    def update_event(self, event_id, title, description, start_time, end_time, location=None):
        """Update an existing calendar event."""
        try:
            event = self.service.events().get(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()
            
            event['summary'] = title
            event['description'] = description
            event['start'] = {
                'dateTime': start_time.isoformat(),
                'timeZone': 'America/New_York',
            }
            event['end'] = {
                'dateTime': end_time.isoformat(),
                'timeZone': 'America/New_York',
            }
            
            if location:
                event['location'] = location
            
            updated_event = self.service.events().update(
                calendarId=self.calendar_id,
                eventId=event_id,
                body=event
            ).execute()
            
            print(f"Updated event: {title} at {start_time}")
            return updated_event['id']
        except HttpError as error:
            print(f"An error occurred updating event: {error}")
            return None
    
    def delete_event(self, event_id):
        """Delete a calendar event."""
        try:
            self.service.events().delete(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()
            print(f"Deleted event: {event_id}")
            return True
        except HttpError as error:
            print(f"An error occurred deleting event: {error}")
            return False
    
    def list_events(self, time_min=None, time_max=None):
        """List events in the calendar."""
        if time_min is None:
            time_min = datetime.utcnow()
        if time_max is None:
            time_max = time_min + timedelta(days=Config.FORECAST_DAYS)
        
        try:
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=time_min.isoformat() + 'Z',
                timeMax=time_max.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return events_result.get('items', [])
        except HttpError as error:
            print(f"An error occurred listing events: {error}")
            return []
    
    def find_event_by_title(self, title, time_min=None, time_max=None):
        """Find an event by its title."""
        events = self.list_events(time_min, time_max)
        for event in events:
            if event.get('summary') == title:
                return event
        return None


