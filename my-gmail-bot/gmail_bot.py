import os
import pickle
import time
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google import genai
from config import GEMINI_API_KEY

# הרשאות ל-Gmail וגם ל-Calendar
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar'
]

def get_services():
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)
    
    gmail_service = build('gmail', 'v1', credentials=creds)
    cal_service = build('calendar', 'v3', credentials=creds)
    return gmail_service, cal_service

def create_event(service, summary, start_time):
    # start_time צריך להיות בפורמט 'YYYY-MM-DDTHH:MM:SS'
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Jerusalem'},
        'end': {'dateTime': start_time, 'timeZone': 'Asia/Jerusalem'},
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'פגישה נקבעה: {event.get("htmlLink")}')

def process_unread_emails():
    gmail_service, cal_service = get_services()
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    results = gmail_service.users().messages().list(userId='me', q='is:unread').execute()
    messages = results.get('messages', [])
    
    for msg in messages:
        email = gmail_service.users().messages().get(userId='me', id=msg['id']).execute()
        content = email['snippet']
        
        # מבקשים מג'מיני להחזיר תשובה בפורמט JSON כדי שנוכל להשתמש בזה בקוד
        prompt = f"""Analyze this email: '{content}'. 
        Extract event title and start time (ISO format YYYY-MM-DDTHH:MM:SS).
        Return ONLY valid JSON like this: {{"title": "...", "time": "..."}}"""
        
        try:
            response = client.models.generate_content(model='gemini-2.0-flash-lite', contents=prompt)
            data = json.loads(response.text.replace("```json", "").replace("```", ""))
            
            create_event(cal_service, data['title'], data['time'])
            
        except Exception as e:
            print(f"שגיאה בעיבוד: {e}")

if __name__ == '__main__':
    process_unread_emails()