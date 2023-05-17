import cv2
import base64
import pytesseract
import os
from dotenv import load_dotenv

load_dotenv()
pytesseract.pytesseract.tesseract_cmd = os.getenv("tesseractPath")

def preprocessImage(image):
    grayedImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    noiseReducedImage = cv2.GaussianBlur(grayedImage, (5, 5), 0)
    preprocessedImage = cv2.adaptiveThreshold(noiseReducedImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    return preprocessedImage

def extractTextFromImage(image):
    custom_config = r'--oem 3 -l eng'
    extractedText = pytesseract.image_to_string(image,config=custom_config)
    return extractedText

def getBase64String(image):
    # Convert the image to a base64-encoded string
    _, buffer = cv2.imencode('.png', image)
    base64Image = base64.b64encode(buffer).decode('utf-8')
    return base64Image