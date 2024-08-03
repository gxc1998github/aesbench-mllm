import pandas as pd
import json

# Load the CSV file
csv_file_path = '/Users/daniel/BIQ2021/Selected_Images_Subset.csv'
try:
    csv_df = pd.read_csv(csv_file_path)
except Exception as e:
    print(f"Error loading CSV file: {e}")
    raise

# Define the JSON structure based on the provided template
json_template = {
    "AesA1_data": {
        "Question": "How is the aesthetic quality of this image?",
        "Options": "A) High\nB) Medium\nC) Low"
    }
}

# Create a dictionary for the JSON file
json_data = {}
for _, row in csv_df.iterrows():
    image_name = row['Image Name']
    json_data[image_name] = json_template

# Save the JSON data to a file
output_json_path = '/Users/daniel/BIQ2021/AesBench_evaluation_subset.json'
try:
    with open(output_json_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    print(f"JSON file successfully saved to {output_json_path}")
except Exception as e:
    print(f"Error saving JSON file: {e}")