from flask import Flask, send_from_directory, request, jsonify
import os
from PIL import Image
from flask_cors import CORS
import json

# Initialize constants
UPLOAD_FOLDER = './uploads'
DOCUMENT_WIDTH = 2481
DOCUEMNT_HEIGHT = 3509

# Initialize Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Enable CORS
CORS(app)

# Entry point route handler
@app.route('/')
def index():
    return 'Hello world'

# Serve pdf document
@app.route('/document')
def provide_document():
    # Create pdf out of the provided images in images directory
    imageList = []
    for image in os.listdir("./uploads/images"):
        if image.endswith(".png"):
            tempImage = Image.open(os.path.join("./uploads/images", image))
            imageConverted = tempImage.convert('RGB')
            imageConverted.filename = tempImage.filename
            imageList.append(imageConverted)
    imageList.sort(key=lambda x: x.filename)
    firstImage = imageList[0]
    imageList.remove(firstImage)
    firstImage.save(r'uploads/output.pdf', save_all=True, append_images=imageList)
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                                    "output.pdf")

# Handle search request for search term and return locations in pdf
@app.route('/document/search', methods=['POST'])
def search_document():
    if request.form:
        searchTerm = request.form.get('q')
        width = float(request.form.get('width'))
        height = float(request.form.get("height"))
        results = []
        with open('./uploads/tokens.json') as json_file:
            data = json.load(json_file)
        for value in data.values():
            if searchTerm in value["text"].lower():
                new_value = dict()
                new_value['x1'] = float(value['x1']) / DOCUMENT_WIDTH * width
                new_value['x2'] = float(value['x2']) / DOCUMENT_WIDTH * width
                new_value['y1'] = float(value['y1']) / DOCUEMNT_HEIGHT * height
                new_value['y2'] = float(value['y2']) / DOCUEMNT_HEIGHT * height
                new_value["page"] = value["page"]
                results.append(new_value)
        return jsonify(results)
    else:
        return "Error, please provide a valid searchTerm, width and height"
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')