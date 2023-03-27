from flask import Flask, render_template, request, jsonify
import base64
import cv2
import numpy as np
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    img_data = request.form.to_dict()
    img_data = img_data["image_data"]
    img_bytes = base64.b64decode(img_data)
    img_np = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    cv2.imwrite('img.jpg', img)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
