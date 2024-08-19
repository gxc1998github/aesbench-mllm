import google.generativeai as genai
import PIL.Image
import torch
import json, time, os
from dotenv import load_dotenv
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the API Key
load_dotenv()
genai.configure(api_key=os.getenv('API_KEY'))
api_key=os.getenv('API_KEY')

# Class for gpt object and define model type
class gptRequest():
    def __init__(self) -> None:
        self.model = genai.GenerativeModel('gemini-1.5-flash')
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

if True:

    # Locate where is the dataset
    #path = "/Users/daniel/Datasets/EAPD/images"
    path = "/Users/daniel/Datasets/BIQ2021/Images"

    # Locate where to record the output
    save_name= "test_AesA3.json"

    # Open the questions and instructions to be asked
    f = open(r"AesBench_evaluation_subset.json", encoding='utf-8')
    data=json.load(f)
    f.close()

    # Create empty answer object and gpt object
    answers={}
    gpt_request = gptRequest()

    # Total questions
    all_num = len(data)

    # Count image number and starting time of the process
    img_num = 1
    start_time = time.time()

    #####------- Pre-Prompt File--------------------------
    # Read the content from the file
    with open('../pre_prompts/pre_prompt3.txt', 'r') as file:
        pre_prompt = file.read()

    #####-------AesA1--------------------------------------
    for imgName, label in data.items():

        # Show the image name
        print(f"\nImage name: {imgName}")

        # Locate the image path inside dataset folder
        img_path = os.path.join(path, imgName)

        # Locate the question to be asked from json file
        AesA3_data = label['AesA3_data']
        AesA3_prompt = AesA3_data['Question'] + "\nYou should output a correct option.\n"
        print(AesA3_prompt)

        # Wait for response
        start = time.time()
        time.sleep(1)
        
        # Send request to API: Pre-Prompt + Prompt + Image
        AesA3_message = gpt_request.forward((pre_prompt+AesA3_prompt), img_path)

        # Show the answer received from API
        print(f"Model Response: \n{AesA3_message}")

        # Record the answer
        answers[imgName] = {"AesA3_response": AesA3_message}

        # Write the answer into a json file
        answers_dict = json.dumps(answers, indent=4)
        with open(save_name, 'w') as outfile:
            outfile.write(answers_dict)

        # Calculate the process time
        avg_time = (time.time() - start_time) / img_num
        need_time = (avg_time * (all_num - img_num)) / 60

        # Show the process time
        print(f"AesA3--{img_num}/{all_num} finished. Using time (s):{time.time() - start:.1f}. Average image time (s):{avg_time:.1f}. Need time (min):{need_time:.1f}.")
                
        # Increment image number, and go to next image for aesthetic evaluation task
        img_num = img_num + 1

