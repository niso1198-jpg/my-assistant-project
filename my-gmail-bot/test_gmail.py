from googleapiclient.discovery import build
import pickle
import os

def check_gmail_only():
    if not os.path.exists('token.json'):
        print("לא נמצא token.json - תריץ קודם את gmail_bot.py כדי לייצר אותו")
        return

    with open('token.json', 'rb') as token:
        creds = pickle.load(token)
    
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', q='is:unread', maxResults=1).execute()
    messages = results.get('messages', [])

    if not messages:
        print("החיבור לג'ימייל עובד, אבל אין מיילים לא קרואים.")
    else:
        print(f"החיבור לג'ימייל עובד! מצאתי מייל עם מזהה: {messages[0]['id']}")

if __name__ == '__main__':
    check_gmail_only()