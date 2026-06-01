import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Try various models that are likely to have free tier quota
models_to_test = [
    'gemini-pro',
    'gemini-pro-latest',
    'gemini-flash-latest',
    'gemini-1.5-pro',
    'gemini-1.5-flash',
    'gemini-2.0-flash'
]

print("Testing models for free tier quota...")
for model_name in models_to_test:
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'OK'")
        print(f"[SUCCESS] {model_name}: {response.text.strip()}")
        break # Found a working one
    except Exception as e:
        print(f"[FAILED]  {model_name}: {str(e)}")
