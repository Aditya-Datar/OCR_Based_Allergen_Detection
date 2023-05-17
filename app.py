from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from pymongo import MongoClient
import base64
import cv2
import numpy as np
from ocrEngine.allergenDetector import checkUserAllergens
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.secret_key = SECRET_KEY

allergens = ["rice", "quinoa", "oats", "corn", "potatoes", "fruits", "vegetables", "nuts", "seeds", "legumes"]
# Configure the MongoDB database
mongo = MongoClient(MONGO_URI)
db = mongo["OcrAllergenDbCluster"]

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = db.users.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            session['email'] = email
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message='Invalid email or password')
    else:
        if 'email' in session:
            return render_template('index.html')
        else:
            return render_template('login.html')

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullName = request.form['name'].strip()
        email = request.form['email'].strip()
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        query = {
            "$or": [
                {"email": email}
            ]
        }
        # Check if username already exists
        user = db.users.find_one(query)
        if user is not None:
            return render_template('login.html', message='Email already exists')
        else:
            # Insert new user to the database
            db.users.insert_one({'email': email, 'password': password,'fullName':fullName})
            session['email'] = email
            return redirect(url_for('profile'))
    else:
        return render_template('register.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

# Index page
@app.route('/')
def index():
    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        return render_template('index.html',user=user)
    else:
        return render_template('index.html')

# Upload endpoint
@app.route('/upload', methods=['POST'])
def upload():
    if 'email' in session:
        img_data = request.form.to_dict()
        imgWidth = img_data["windowWidth"]
        imgHeight = img_data["windowHeight"]
        base64image = img_data["image_data"]

        img_bytes = base64.b64decode(base64image)
        img_np = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        filepath = os.path.join('uploads', 'img.jpg')
        print("filepath is" + filepath)
        cv2.imwrite(filepath, img)

        user = db.users.find_one({'email': session['email']})
        userAllergens = user['allergenCategory'] + user['otherAllergenList']
        finalResponse = jsonify({'status': checkUserAllergens(userAllergens, filepath, base64image, imgWidth, imgHeight)})
        
        return finalResponse
    else:
        return redirect(url_for('login'))

# Profile page
@app.route('/profile')
def profile():
    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        if user:
            del user["_id"]
            print(user)
            return render_template('profile.html', user=user)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

# Update profile endpoint
@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'email' in session:
        fullName = request.form.get('fullname').strip()
        email = request.form.get('email').strip()
        mobile = request.form.get('mobileNo').strip()
        gender = request.form.get('gender')
        age = request.form.get('age')
        allergenCategory = request.form.getlist('allergens')
        otherAllergenList = request.form.get('otherAllergen').split(",")
        allergenCategoryList = request.form.get('allergenList').split(",")
        user = db.users.find_one({'email': session['email']})
        if user:
            updatedUserDetails = {'fullName':fullName, 'email':email, 'mobile':mobile, 'gender':gender, 'age':age, 'allergenCategory':allergenCategory,'allergenCategoryList':allergenCategoryList, 'otherAllergenList':otherAllergenList}
            db.users.update_one({'email': session['email']}, {'$set': updatedUserDetails})
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
