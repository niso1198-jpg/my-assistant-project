from google import genai
import arabic_reshaper
from bidi.algorithm import get_display
from config import GEMINI_API_KEY

# יצירת הלקוח
client = genai.Client(api_key=GEMINI_API_KEY)

def test_prompt(email_content):
    prompt = f"""
    Analyze this email and extract: Sender Name, Location, and Time.
    Return the output in Hebrew.
    Format:
    שם השולח: [Name]
    מיקום: [Location]
    שעה: [Time in LTR format like 15:30]
    
    Email: {email_content}
    """
    
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt
    )
    return response.text

# תוכן לבדיקה
sample_email = "Hi, I'm Niso from Tel Aviv, let's meet at 15:30 to discuss the project."

# קבלת התוצאה
raw_text = test_prompt(sample_email)

# תיקון תצוגת העברית (הפיכת האותיות והכיווניות)
reshaped_text = arabic_reshaper.reshape(raw_text)
bidi_text = get_display(reshaped_text)

# הדפסה סופית
print(bidi_text)