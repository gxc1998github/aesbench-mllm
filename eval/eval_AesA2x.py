import google.generativeai as genai
import os
import PIL.Image
import torch
import csv, time, json
from dotenv import load_dotenv

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the API Key
load_dotenv()
genai.configure(api_key=os.getenv('API_KEY'))
api_key = os.getenv('API_KEY')

# Class for gpt object and define model type
class GptRequest:
    # Constructor
    def __init__(self) -> None:
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    # Function to forward message
    def forward(self, prompt, image_path, server='Gemini'):
        if server == 'Gemini':
            img = PIL.Image.open(image_path)
            text = ""
            
            while len(text.strip()) < 3:
                try:
                    response = self.model.generate_content([prompt, img])
                    response.resolve()
                    
                    # Inspect response object to get text
                    result = response._result  
                    if result.candidates:
                        text_content = result.candidates[0].content.parts[0].text
                        text = text_content if text_content else ""
                    else:
                        text = ""
                        
                except Exception as error:
                    print(error)
                    print('Sleeping for 10 seconds')
                    time.sleep(10)
                        
        return text

# Show what computing power is used
print(f"\n*** Currently is using: {device} ***")

# Create empty answer object and gpt object
answers = {}
gpt_request = GptRequest()

# Please download the dataset
# >> Locate where is the dowloaded image dataset:
path = "/Users/daniel/Datasets/BIQ2021/Images"

# >> Locate where to record the gpt output
save_name = "test_AesA2.json"

# >> Locate pre-prompt File:
with open('../pre_prompts/pre_prompt2.txt', 'r') as file:
    pre_prompt = file.read()

# AesA2 Process
# >> Locate list of 100 image names
with open('../data_release/ground_truth.csv', mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header if there is one
    
    img_num = 1
    start_time = time.time()

    for row in reader:
        imgName = row[0]  # Assuming the image name is in the first column

        # Show the image name
        print(f"\nImage name: {imgName}")

        # Locate the image path inside dataset folder
        img_path = os.path.join(path, imgName)

        # Placeholder question
        AesA2_prompt = "How is the aesthetic quality of this image? Give a score with a scale of 1 to 5."
        print(AesA2_prompt)

        # Wait for response
        start = time.time()
        time.sleep(1)
        
        # Send request to API: Pre-Prompt + Prompt + Image
        AesA2_message = gpt_request.forward((pre_prompt + AesA2_prompt), img_path)

        # Show the answer received from API
        print(f"\n{AesA2_message}")

        # Record the answer
        answers[imgName] = {"AesA2_response": AesA2_message}

        # Write the answer into a json file
        with open(save_name, 'w') as outfile:
            json.dump(answers, outfile, indent=4)

        # Calculate the process time
        avg_time = (time.time() - start_time) / img_num
        need_time = (avg_time * (len(answers) - img_num)) / 60

        # Show the process time
        print(f"AesA2--{img_num}/{len(answers)} finished. Using time (s):{time.time() - start:.1f}. Average image time (s):{avg_time:.1f}. Need time (min):{need_time:.1f}.")
                
        # Increment image number, and go to next image for aesthetic evaluation task
        img_num += 1