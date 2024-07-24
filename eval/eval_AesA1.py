from dotenv import load_dotenv
import torch
from PIL import Image
device = "cuda" if torch.cuda.is_available() else "cpu"
import json, time, os
import google.generativeai as genai
import PIL.Image

# Load the API Key
load_dotenv()
genai.configure(api_key=os.getenv('API_KEY'))
api_key=os.getenv('API_KEY')

# Class for gpt object and define model type
class gptRequest():
    def __init__(self) -> None:
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    def forward(self, prompt, image_path,  server='Gemini'):
        if server == 'Gemini':
            img = PIL.Image.open(image_path)
            text = ""
            while len(text) < 3:
                try:
                    response = self.model.generate_content([prompt, img], stream=True)
                    response.resolve()
                    try:
                        text = response.text.strip()
                    except:
                        text = " "
                except Exception as error:
                    print(error)
                    print('Sleeping for 10 seconds')
                    time.sleep(10)
                    text = text+" "

        return text

# Show what computing power is used
print(f"\n*** Currently is using: {device} ***")

if True:

    # Locate where is the dataset
    path = "/Users/daniel/EAPD/images"

    # Locate where to record the output
    save_name= "test_AesA1.json"

    # Open the questions and instructions
    f = open(r"AesBench_evaluation.json", encoding='utf-8')
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

    #####-------AesA1--------------------------
    for imgName, label in data.items():

        # Show the image name
        print(f"\nImage name: {imgName}")

        # Locate the image path inside dataset folder
        img_path = os.path.join(path, imgName)

        # Locate the question to be asked from json file
        AesA1_data = label['AesA1_data']
        AesA1_prompt = AesA1_data['Question'] + "\nChoose one from the following options:\n" + AesA1_data['Options'] + "\nYou should output a correct option.\n"
        print(AesA1_prompt)

        # Wait for response
        start = time.time()
        time.sleep(1)
        
        # Send request to API
        AesA1_message = gpt_request.forward(AesA1_prompt, img_path)

        # Show the answer received from API
        print(f"Answer:\n{AesA1_message}")

        # Record the answer
        answers[imgName] = {"AesA1_response": AesA1_message}

        # Write the answer into a json file
        answers_dict = json.dumps(answers, indent=4)
        with open(save_name, 'w') as outfile:
            outfile.write(answers_dict)

        # Calculate the process time
        avg_time = (time.time() - start_time) / img_num
        need_time = (avg_time * (all_num - img_num)) / 3600

        # Show the process time
        print(f"AesA1--{img_num}/{all_num} finished. Using time (s):{time.time() - start:.1f}. Average image time (s):{avg_time:.1f}. Need time (h):{need_time:.1f}.")
        
        # Increment image number, and go to next image for aesthetic evaluation task
        img_num = img_num + 1

