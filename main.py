import cv2
import pytesseract
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
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

def take_picture():
    # Code for taking picture from camera goes here
    # Open the camera
    cap = cv2.VideoCapture(0)

    # Capture a single frame
    ret, frame = cap.read()

    # Release the camera
    cap.release()

    # Save the frame as a jpeg file
    cv2.imwrite("captured_image.jpg", frame)

    return "captured_image.jpg"

def choose_file():
    root.filename = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("jpeg files", ".jpg"), ("all files", ".*")))
    return root.filename

def check_allergens():
    allergens = entry.get().split(',')
    image_path = None
    if var.get() == 1:
        image_path = choose_file()
    elif var.get() == 2:
        image_path = take_picture()
        # image_path = "path_to_saved_image.jpg"

    ingredients = extract_text_from_image(image_path)
    result = compare_ingredients(ingredients, allergens)
    messagebox.showinfo("Result", result)

root = tk.Tk()
root.geometry("400x200")
root.title("Allergen Checker")

label = tk.Label(root, text="Enter allergens separated by comma:")
entry = tk.Entry(root)
check_button = tk.Button(root, text="Check", command=check_allergens)
var = tk.IntVar()
file_option = tk.Radiobutton(root, text="Select file", variable=var, value=1)
camera_option = tk.Radiobutton(root, text="Take picture", variable=var, value=2)
file_option.pack()
camera_option.pack()

label.pack()
entry.pack()
check_button.pack()

root.mainloop()
