import os
import sys
import requests
from dotenv import load_dotenv
from nltk.tokenize import word_tokenize
from ocrEngine.imageProcessing import getBase64String

load_dotenv()

def getIngredientsFromExtractedText(image, text):
    text = getOcrImageText(image)
    print("Extracted Text " + text)
    tokens = word_tokenize(text)
    # Filter out non-ingredient words and return the list of ingredients
    stopWords = ["and", "of", "with", "in", "to", "for", "on", "per", "serving", "each", "product", "packet", "ingredients"]

    ingredientsList = [token for token in tokens if token.lower() not in stopWords]

    print("ingredientsList" + ingredientsList)
    return ingredientsList
    
def getOcrImageText(image):
    # Set up the OCR.space API endpoint and parameters
    url = 'https://api.ocr.space/parse/image'
    payload = {'apikey': os.getenv("tesseractKey"),'language': 'eng','isOverlayRequired': False,'base64Image': f'data:image/jpeg;base64,{getBase64String(image)}'}
    if(sys.getsizeof(payload) < 1024000):
        # Send the POST request to OCR.space API
        response = requests.post(url, data=payload)
        # Parse the JSON response to extract the text
        if response.status_code == 200:
            text = ""
            result = response.json()
            if result['ParsedResults']:
                text = result['ParsedResults'][0]['ParsedText']
            return text
        else:
            print('Error:', response.status_code)

    return ""   
    