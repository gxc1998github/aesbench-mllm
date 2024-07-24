import google.generativeai as genai
import os

apiKeyAI = "pip "
apiKeyGoogleCloud = "AIzaSyDetIFrg5lEACtNdJYeIYKbAZxseYseAuo" 

#genai.configure(api_key=apiKeyAI)
genai.configure(api_key=apiKeyGoogleCloud)

#model = genai.GenerativeModel('gemini-1.5-flash') 
model = genai.GenerativeModel('gemini-1.5-pro')    


response = model.generate_content("Write a story about an AI and magic, make it one sentence.")

# Access the result attribute of the response
result = response._result

# Access the first candidate's content parts and text
text_content = result.candidates[0].content.parts[0].text

print(text_content)