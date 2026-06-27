from google import genai
from config import GEMINI_API_KEY

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
    print("בודק חיבור ל-Gemini...")
    response = client.models.generate_content(model='gemini-2.0-flash-lite', contents="hello")
    print("החיבור ל-Gemini עובד!")
except Exception as e:
    print(f"שגיאת חיבור: {e}")