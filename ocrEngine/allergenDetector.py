import cv2
from ocrEngine.imageProcessing import preprocessImage, extractTextFromImage
from ocrEngine.textProcessor import getIngredientsFromExtractedText

def getIngredientsList(filepath, image_path, imgWidth, imgHeight):
    image = cv2.imread(filepath)
    image = cv2.resize(image, (int(float(imgWidth)), int(float(imgHeight))))
    # cv2.imshow('image', image)
    # cv2.waitKey(0)

    if image is None or image.size == 0:
        raise ValueError("The image could not be loaded. Please check the file path and make sure the file exists.")

    preProcessedImage = preprocessImage(image)
    extractedText = extractTextFromImage(preProcessedImage)
    ingredientsList = getIngredientsFromExtractedText(image_path,extractedText)

    return ingredientsList

def compareIngredients(ingredientsList, userAllergens):

    # Convert the ingredients and allergens to lowercase for case-insensitive comparison
    ingredientsList = [ingredient.lower() for ingredient in ingredientsList]

    # print(ingredients)
    userAllergens = [allergen.lower() for allergen in userAllergens]

    # Check if any of the allergens are present in the ingredients list
    for allergen in userAllergens:
        for ingredient in ingredientsList:
            if allergen in ingredient:
                return False
    return True

def checkUserAllergens(userAllergens, filepath, image_path, imgWeight, imgHeight):
    ingredientsList = getIngredientsList(filepath, image_path, imgWeight, imgHeight)
    result = compareIngredients(ingredientsList, userAllergens)
    return result