import cv2
from ocrEngine.imageProcessing import preprocessImage, extractTextFromImage
from ocrEngine.textProcessor import getIngredientsFromExtractedText

def getIngredientsList(image_path):
    image = cv2.imread(image_path)
    if image is None or image.size == 0:
        raise ValueError("The image could not be loaded. Please check the file path and make sure the file exists.")
    
    preProcessedImage = preprocessImage(image)
    extractedText = extractTextFromImage(preProcessedImage)
    ingredientsList = getIngredientsFromExtractedText(image,extractedText)
    return ingredientsList

def compareIngredients(ingredientsList, userAllergens):

    # Convert the ingredients and allergens to lowercase for case-insensitive comparison
    ingredientsList = [ingredient.lower() for ingredient in ingredientsList]

    # print(ingredients)
    userAllergens = [allergen.lower() for allergen in userAllergens]
    
    # Check if any of the allergens are present in the ingredients list
    for allergen in userAllergens:
        if allergen in ingredientsList:
            return False
    return True

def checkUserAllergens(userAllergens, image_path):
    ingredientsList = getIngredientsList(image_path)
    result = compareIngredients(ingredientsList, userAllergens)
    if result:
        return "Product is safe to use ✅"
    
    return "Product is not safe to use ❌"