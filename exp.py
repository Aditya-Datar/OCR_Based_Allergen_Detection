import requests

def ocr_space_file(filename, api_key, language='eng'):
    payload = {'language': language}
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image', 
                          files={filename: f},
                          data=payload,
                          headers={'apikey': api_key})
    return r.content.decode()

# Provide your API key obtained from OCR.space
api_key = 'K82411896588957'

# Provide the filename of the image you want to extract text from
filename = r"C:\Users\Aditya Datar\Desktop\Semester 8\Final Year Project\Codes\static\img\garlic.jpeg"

# Perform OCR and get the extracted text
extracted_text = ocr_space_file(filename, api_key)

# Print the extracted text
print(extracted_text)

import cv2
import requests
import base64

# Load the image using cv2
image = cv2.imread('example.png')

# Convert the image to a base64-encoded string
retval, buffer = cv2.imencode('.png', image)
b64_image = base64.b64encode(buffer).decode('utf-8')

# Set up the OCR.space API endpoint and parameters
url = 'https://api.ocr.space/parse/image'
apikey = 'abc123'
payload = {'apikey': apikey,
           'language': 'eng',
           'isOverlayRequired': False,
           'base64Image': b64_image}

# Send the POST request to OCR.space API
response = requests.post(url, data=payload)

# Parse the JSON response to extract the text
if response.status_code == 200:
    result = response.json()
    text = result['ParsedResults'][0]['ParsedText']
    print(text)
else:
    print('Error:', response.status_code)
