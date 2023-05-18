import os
import sys
import requests
import base64
from dotenv import load_dotenv
from ocrEngine.imageCompression import compress_image
from ocrEngine.textSpeller import correct_spelling


load_dotenv()

def getIngredientsFromExtractedText(image, text):
    text = getOcrImageText(image)
    # print(type(text))
    print("Extracted Text " + text)
    tokens = text.split(",")
    print(tokens)

    # Filter out non-ingredient words and return the list of ingredients
    stopWords = ["and", "of", "with", "in", "to", "for", "on", "per", "serving", "each", "product", "packet", "ingredients"]

    ingredientsList = [token for token in tokens if token.lower() not in stopWords]

    for i in range(len(ingredientsList)):
        ingredientsList[i] = ingredientsList[i].strip()
        ingredientsList[i] = correct_spelling(ingredientsList[i])
        ingredientsList[i] = ingredientsList[i].replace("\r", "")
        ingredientsList[i] = ingredientsList[i].replace("\n", " ")
        ingredientsList[i] = ingredientsList[i].replace("\\", "")

    print("ingredientsList" + str(ingredientsList))
    return ingredientsList

def getOcrImageText(image):
    with open(os.getenv("imgPath"), "wb") as fh:
        fh.write(base64.decodebytes(bytes(image, 'utf-8')))
    compress_image(os.getenv("imgPath"), 1024000)

    payload = {'apikey': os.getenv("tesseractKey"),'language': 'eng','isOverlayRequired': False}

    with open(os.getenv("imgPath"), 'rb') as f:
        response = requests.post(os.getenv("url"), files={os.getenv("imgPath"): f}, data=payload)

    if response.status_code == 200:
        text = ""
        result = response.json()
        if result['ParsedResults']:
            text = result['ParsedResults'][0]['ParsedText']
        return text
    else:
        print('Error:Something went wrong')

    return ""
