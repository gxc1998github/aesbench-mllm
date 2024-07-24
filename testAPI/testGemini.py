from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()
genai.configure(api_key=os.getenv('API_KEY'))
api_key=os.getenv('API_KEY')

#model = genai.GenerativeModel('gemini-1.5-flash') 
model = genai.GenerativeModel('gemini-1.5-pro')    

response = model.generate_content("Write a story about education, make it one sentence.")

# Access the result attribute of the response
result = response._result

# Access the first candidate's content parts and text
text_content = result.candidates[0].content.parts[0].text

print("\n" + text_content)