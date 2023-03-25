import cv2
import pytesseract
from nltk.tokenize import word_tokenize

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    # Load the image and convert it to grayscale
    image = cv2.imread(image_path)
    if image is None or image.size == 0:
        raise ValueError("The image could not be loaded. Please check the file path and make sure the file exists.")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    # gray = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply OTSU threshold to make the text more distinguishable
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Use Tesseract OCR to extract text from the image
    text = pytesseract.image_to_string(threshold)
    
    # Tokenize the text to separate out the ingredients
    tokens = word_tokenize(text)
    
    # Filter out non-ingredient words and return the list of ingredients
    stop_words = ["and", "of", "with", "in", "to", "for", "on", "per", "serving", "each", "product", "packet", "ingredients"]
    ingredients = [token for token in tokens if token.lower() not in stop_words]
    return ingredients

def compare_ingredients(ingredients, allergens):
    # Convert the ingredients and allergens to lowercase for case-insensitive comparison
    ingredients = [ingredient.lower() for ingredient in ingredients]
    print(ingredients);
    allergens = [allergen.lower() for allergen in allergens]
    
    # Check if any of the allergens are present in the ingredients list
    for allergen in allergens:
        if allergen in ingredients:
            return "Product is not safe for use"
    return "Product is safe for use"

def check_allergens(allergens, image_path):
    ingredients = extract_text_from_image(image_path)
    result = compare_ingredients(ingredients, allergens)
    return result