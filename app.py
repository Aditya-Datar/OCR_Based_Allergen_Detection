from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from pymongo import MongoClient
import base64
import cv2
import numpy as np
from allergenDetector import check_allergens
import os
from dotenv import load_dotenv


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
        print(request.form)
        email = request.form['email']
        password = request.form['password']
        user = db.users.find_one({'email': email})
        if user and user['password'] == password:
            session['email'] = email
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message='Invalid username or password')
    else:
        if 'email' in session:
            return render_template('index.html')
        else:
            return render_template('login.html')

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullName = request.form['name']
        email = request.form['email']
        password = request.form['password']
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
    if 'username' in session:
        img_data = request.form.to_dict()
        img_data = img_data["image_data"]
        img_bytes = base64.b64decode(img_data)
        img_np = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        img = cv2.flip(img,1)
        filepath = os.path.join('uploads', 'img.jpg')
        cv2.imwrite(filepath, img)
        finalResponse = jsonify({'status': check_allergens(allergens, filepath)})
        os.remove(filepath)
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
    # allergenDict = {
    #     "Gluten":["rice", "quinoa", "oats", "corn", "potatoes", "fruits", "vegetables", "nuts", "seeds", "legumes"],
    #     "Dairy":["almond", "soy","coconut","oat milk","cheese", "yogurt", "ice cream","butter", "cream","dried milk","milk solids","powered milk","whey"],
    #     "Nut" : ["pumpkin", "sunflower","sesame seeds","snack mixes","dried fruits","raisins","date","prunes","figs","apricots","peaches"],
    #     "Soy" : ["almond milk", "coconut milk", "oat milk"],
    #     "Meat Based": ["egg", "fish","red meat","chicken","mutton"],
    #     "Fruit Based":["Apple","Avocado","Banana","Cherry","Kiwi","Mango","Melon","Nectraine","Peach","Pear","Pineapple","strawberry","Plum","Tomato","Jackfruit"],
    #     "Cruciferous" : ["Broccoli","cauliflower","cabbage","kale","collard greens","kohlrabi"]
    #     }
    if 'email' in session:
        fullName = request.form.get('fullname')
        email = request.form.get('email')
        mobile = request.form.get('mobileNo')
        gender = request.form.get('gender')
        age = request.form.get('age')

        allergenCategory = request.form.getlist('allergens')

        otherAllergenList = request.form.get('otherAllergen').split(",")
        allergenCategoryList = request.form.get('allergenList').split(",")
        # finalAllergenList = []
        # print(otherAllergenList)
        # print("Allergen Category ", allergenCategory)
        # for allergen in allergenCategory:
        #     finalAllergenList += allergenDict[allergen]
        # if otherAllergenList[0] != '':
        #     finalAllergenList.append(otherAllergenList)
        user = db.users.find_one({'username': session['username']})
        if user:
            updatedUserDetails = {'fullName':fullName, 'email':email, 'mobile':mobile, 'gender':gender, 'age':age, 'allergenCategory':allergenCategory,'allergenCategoryList':allergenCategoryList, 'otherAllergenList':otherAllergenList}
            db.users.update_one({'username': session['username']}, {'$set': updatedUserDetails})
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    # app.run(host="0.0.0.0",port=5000,ssl_context="adhoc",threaded=True)
    app.run(debug=True)
