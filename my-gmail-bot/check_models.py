from google import genai
from config import GEMINI_API_KEY

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
    print("מתחבר ל-API...")
    models = client.models.list()
    for model in models:
        print(f"Model Name: {model.name}")
except Exception as e:
    print(f"שגיאה בחיבור: {e}")