from flask import Flask, render_template, request, jsonify
import base64
import cv2
import numpy as np
import json
from allergenDetector import check_allergens
import os

app = Flask(__name__)
allergens = ['milk', 'soya']

@app.route('/')
def index():
    return render_template('demoVideoCanvas.html')

@app.route('/upload', methods=['POST'])
def upload():
    img_data = request.form.to_dict()
    img_data = img_data["image_data"]
    img_bytes = base64.b64decode(img_data)
    img_np = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    img = cv2.flip(img,1)
    filepath = os.path.join('uploads', 'img.jpg')
    cv2.imwrite(filepath, img)
    return jsonify({'status': check_allergens(allergens, filepath)})

if __name__ == '__main__':
    app.run(debug=True)
