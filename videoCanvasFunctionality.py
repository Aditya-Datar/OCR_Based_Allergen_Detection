from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from pymongo import MongoClient
import base64
import cv2
import numpy as np
import json
from allergenDetector import check_allergens
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

allergens = ['milk', 'soya']
# Configure the MongoDB database
mongo = MongoClient('mongodb+srv://ocr:allergen@cluster0.w5vwpiq.mongodb.net/?retryWrites=true&w=majority')
db = mongo["Cluster0"]
# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.users.find_one({'username': username})
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message='Invalid username or password')
    else:
        return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Index page
@app.route('/')
def index():
    if 'username' in session:
        return render_template('demoVideoCanvas.html')
    else:
        return redirect(url_for('login'))

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
        return jsonify({'status': check_allergens(allergens, filepath)})
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
