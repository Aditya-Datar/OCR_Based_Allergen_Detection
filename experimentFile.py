import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pytesseract
import cv2
import os
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

def text_to_ingredients(text):
    tokens = word_tokenize(text)
    ingredients = [token for token in tokens if token.lower() in allergens]
    return ingredients

allergens = {"flour", "sugar", "butter", "eggs", "milk", "baking powder", "vanilla extract"}

# text = "This recipe calls for 2 cups of flour, 1 cup of sugar, 1/2 cup of butter, 2 eggs, 1/2 cup of milk, 1 teaspoon of baking powder, and 1 teaspoon of vanilla extract."
# ingredients_list = text_to_ingredients(text)
# print(ingredients_list)

# Output: ['flour', 'sugar', 'butter', 'eggs', 'milk', 'baking powder', 'vanilla extract']


# List of allergens
# allergens = ["peanut", "tree nut", "milk", "egg", "soy", "Wheat.", "fish", "shellfish","Gluten"]
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Function to convert image to text
def convert_image_to_text(image_path):
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Otsu thresholding to the grayscale image
    _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Recognize text in the thresholded image
    text = pytesseract.image_to_string(thresholded)
    print(text)
    # Return the recognized text
    return text

# Function to check if the product is safe
def check_product_safety(ingredients_list, allergens):
    print(ingredients_list)
    for allergen in allergens:
        if allergen in ingredients_list:
            return False
    return True

# GUI window
root = tk.Tk()
root.title("Allergy Detection App")

# Label and button to select image
label = tk.Label(root, text="Select image of ingredients")
label.pack()

button = tk.Button(root, text="Select Image", command=lambda: select_image())
button.pack()

# Function to select image
def select_image():
    # file_path = filedialog.askopenfilename()
    # print(file_path)
    ingredients = convert_image_to_text(r"C:\Users\Aditya Datar\Desktop\Semester 8\Final Year Project\Codes\ingredients.jpg")
    ingredients_list = text_to_ingredients(ingredients)
    print(ingredients_list)
    is_safe = check_product_safety(ingredients_list, allergens)
    if is_safe:
        messagebox.showinfo("Result", "Product is safe for use")
    else:
        messagebox.showwarning("Result", "Product is not safe for use")

root.mainloop()