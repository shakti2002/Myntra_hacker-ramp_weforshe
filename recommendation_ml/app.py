from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import random
import json
import pickle
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.models import Sequential
from sklearn.neighbors import NearestNeighbors
from numpy.linalg import norm

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
IMAGE_FOLDER = 'imagefile'
METADATA_FILE = 'metadata.json'
EMBEDDINGS_FILE = 'embeddings_shri.pkl'
FILENAMES_FILE = 'filenames_shri.pkl'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, 'w') as f:
        json.dump([], f)

feature_list = np.array(pickle.load(open(EMBEDDINGS_FILE, 'rb')))
filenames = pickle.load(open(FILENAMES_FILE, 'rb'))

model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model.trainable = False
model = Sequential([
    model,
    GlobalMaxPooling2D()
])

def feature_extraction(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)
    return normalized_result

def recommend(features, feature_list):
    neighbors = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')
    neighbors.fit(feature_list)
    distances, indices = neighbors.kneighbors([features])
    return indices

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        with open(METADATA_FILE, 'r') as f:
            metadata = json.load(f)
        
        new_image = {
            'filename': filename,
            'rating': random.uniform(0, 5),
            'comments': []
        }
        metadata.append(new_image)

        with open(METADATA_FILE, 'w') as f:
            json.dump(metadata, f)

        # Feature extraction and recommendation
        features = feature_extraction(file_path, model)
        indices = recommend(features, feature_list)

        recommended_images = [filenames[idx] for idx in indices[0][1:6]]

        return jsonify({
            'message': 'Image uploaded successfully',
            'recommendations': [f"{os.path.basename(img)}" for img in recommended_images]
        }), 200

@app.route('/images', methods=['GET'])
def get_images():
    sort_by_rating = request.args.get('sort_by_rating', 'false').lower() == 'true'
    with open(METADATA_FILE, 'r') as f:
        metadata = json.load(f)

    if sort_by_rating:
        metadata.sort(key=lambda x: x['rating'], reverse=True)

    return jsonify(metadata), 200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/imagefile/<filename>')
def image_file(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, port=80)
