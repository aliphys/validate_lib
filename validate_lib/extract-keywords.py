import requests
import csv
import json
import re
import os

# URL of the JavaScript file containing the ARDUINO_KW object
url = "https://raw.githubusercontent.com/highlightjs/highlight.js/063876f86c53713a665de0b17b8d795ae5fce0a1/src/languages/arduino.js"

# Fetching the content of the file
response = requests.get(url)
content = response.text

# Extracting the ARDUINO_KW object
start = content.find("const ARDUINO_KW = {")
end = content.find("};", start) + 1
arduino_kw_js = content[start:end]

# Replace JavaScript object syntax with valid JSON syntax
# Ensuring all object keys are enclosed in double quotes
arduino_kw_json = arduino_kw_js.replace("const ARDUINO_KW = ", "")
arduino_kw_json = re.sub(r'([a-zA-Z_]+):', r'"\1":', arduino_kw_json)  # Enclose keys in double quotes
arduino_kw_json = arduino_kw_json.replace("'", "\"")  # Replace single quotes with double quotes
arduino_kw_json = arduino_kw_json.replace("\"_hints\":", "\"hints\":")  # Remove the underscore from _hints

# Convert the JSON string to a Python dictionary
try:
    arduino_kw_dict = json.loads(arduino_kw_json)
except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {e}")
    exit(1)

# Preparing the CSV data
csv_data = [["Keyword"]]
for category, keywords in arduino_kw_dict.items():
    for keyword in keywords:
        csv_data.append([keyword])

# Define the CSV file path
script_dir = os.path.dirname(os.path.realpath(__file__))  # Directory of the script
csv_file_name = 'arduino_keywords.csv'
csv_file_path = os.path.join(script_dir, csv_file_name)

# Writing the data to a CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)

print(f"Arduino keywords have been saved to {csv_file_path}")
