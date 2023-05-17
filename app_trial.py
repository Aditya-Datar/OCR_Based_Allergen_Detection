from flask import Flask, render_template,request
import cv2
from werkzeug.utils import secure_filename
import sys
import requests
import cv2
import base64

app = Flask(__name__)

@app.route("/accept", methods=['POST', 'GET'])
def func():
    print("Inside func()")
    if request.method == "POST":
        image = request.files['file']
        # print(type(image))
        # filename = secure_filename(image.filename)
        # print(filename)
        image.save("D:\\College\\Semester 8\\Capstone\\OCR_Based_Allergen_Detection\\ocrEngine\\New\\img.jpg")
        getResponse()

    return render_template('trial.html')



def getResponse():
    img = cv2.imread("D:\\College\\Semester 8\\Capstone\\OCR_Based_Allergen_Detection\\ocrEngine\\New\\img.jpg")

    url = 'https://api.ocr.space/parse/image'
    payload = {'apikey': 'K82411896588957','language': 'eng','isOverlayRequired': False,'base64Image': f'data:image/jpeg;base64,{getBase64String(img)}'}
    if(sys.getsizeof(payload) < 1024000):
        # Send the POST request to OCR.space API
        response = requests.post(url, data=payload)
        print("API Response " , response)
        # Parse the JSON response to extract the text
        if response.status_code == 200:
            text = ""
            result = response.json()
            print("API REsponse" , result)
            if result['ParsedResults']:
                text = result['ParsedResults'][0]['ParsedText']
            print(text)
        else:
            print('Error:', response.status_code)

    print("REE")


def getBase64String(image):
    # Convert the image to a base64-encoded string
    _, buffer = cv2.imencode('.jpeg', image)
    base64Image = base64.b64encode(buffer).decode('utf-8')
    return base64Image




if __name__ == '__main__':
    app.run(debug=True)