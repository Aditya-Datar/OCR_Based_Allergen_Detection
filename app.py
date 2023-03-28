import os
from flask import Flask, render_template, request
from allergenDetector import check_allergens

app = Flask(__name__)
allergens = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return 'No image uploaded.', 400
    
    # Create the uploads folder if it doesn't exist already
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    file = request.files['image']
    filename = file.filename
    # Save the file to the "uploads" folder
    filepath = os.path.join('uploads', filename)
    file.save(filepath)
    # Get the allergens list from the form data
    allergens = request.form['allergens'].split(',')
    
    return check_allergens(allergens, filepath)

@app.route('/uploadAllergens', methods=['GET'])
def uploadAllergensGet():
    return render_template('uploadAllergens.html')

@app.route('/uploadAllergens', methods=['POST'])
def uploadAllergens():
    global allergens 
    allergens = request.form['allergens'].split(',')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
