
from flask import Flask, request, jsonify, render_template
from ast import literal_eval
from bson import ObjectId
from pymongo import MongoClient
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
import json
from flask import send_from_directory
from werkzeug.utils import secure_filename
import datetime
import os
app = Flask(__name__)
load_dotenv()

cors = CORS(app, resources={r"/*": {"origins": "*"}})

client = MongoClient(os.getenv('MONGO_URL'))
db = client.get_database('manit')
def convert_object_id(data):
    if isinstance(data, list):
        for item in data:
            item['_id'] = str(item['_id'])
    else:
        data['_id'] = str(data['_id'])
    return data



UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def save_image(image):
    filename = secure_filename(image.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image.save(filepath)
    return f'/uploads/{filename}'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/login", methods=["GET", "POST"])
def Login():
    
    user_input = request.json  # Use request.json to directly parse JSON data
    user_email = user_input["user"]["email"]
    print(user_input["user"]["password"])
    user_password = user_input["user"]["password"]
       
        
    existing_user = db.user.find_one({'email': user_email})
        
    if not existing_user:
        return jsonify({'message': 'No Email exists'}), 400
        
        
    user_db=db.user.find_one({"email":user_email})
        
    if user_db.get('password')==user_password:
            # current_user_details['email'] = existing_user['email']
            # current_user_details['name'] = existing_user['name']
        return jsonify({'message': 'Login successful', 'joined_channels': existing_user.get('joined_channels', [])}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}),401

# @app.route("/signup", methods=["POST"])
# def signup():
#     user_input = request.json  # Use request.json to directly parse JSON data
#     user_email = user_input["email"]
#     user_password = user_input["password"]

#     existing_user = db.user.find_one({'email': user_email})
#     if existing_user:
#         return jsonify({'message': 'Email already exists'}), 400
    
#     try:
#         db.user.insert_one({"email": user_email, "password": user_password})
#     except Exception as e:
#         return jsonify({'message': str(e)}), 500
    
#     return jsonify({'message': 'Registration successful'}), 200


@app.route("/signup", methods=["GET", "POST"])
def Signup():
    if request.method == 'POST':
        user_input = request.data
        user_input=literal_eval(user_input.decode('utf-8'))
        # print(user_input["user"]["email"])
        # print(type(json.loads(user_input["user"])))
        user_input=json.loads(user_input["user"])
        print(user_input)
        # Check if the email is already registered
        #  print(collection.find_one({"_id": ObjectId("59d7ef576cab3d6118805a20")}))
        
        existing_user = db.user.find_one({'email': user_input["email"]})
        
        if existing_user:
            return jsonify({'message': 'Email already exists'}), 400
        try:
           db.user.insert_one({"name":user_input["name"],"email":user_input["email"], "password":user_input["password"]})
        except Exception as e:
            return "Error in db"
        return jsonify({'message': 'Registration successful'}), 200

@app.route("/join_channel", methods=["POST"])
def join_channel():
    data = request.json
    user_email = data['email']
    channel_name = data['channel_name']
    
    user = db.user.find_one({'email': user_email})
    if user:
        if 'joined_channels' not in user:
            user['joined_channels'] = []
        if channel_name not in user['joined_channels']:
            user['joined_channels'].append(channel_name)
            db.user.update_one({'email': user_email}, {'$set': {'joined_channels': user['joined_channels']}})
        
        return jsonify({'message': 'Channel joined', 'joined_channels': user['joined_channels']}), 200
    
    return jsonify({'message': 'User not found'}), 404


@app.route("/joined_channels", methods=["POST"])
def get_joined_channels():
    user_input = request.data
    user_input = literal_eval(user_input.decode('utf-8'))
    
    email = user_input["email"]
    
    user_db = db.user.find_one({"email": email})
    if not user_db:
        return jsonify({'message': 'User not found'}), 400
    
    joined_channels = user_db.get("joined_channels", [])
    return jsonify({'joined_channels': joined_channels}), 200


@app.route("/like", methods=["POST"])
def like():
    data = request.json
    comment_id = ObjectId(data['comment_id'])
    db.comments.update_one({'_id': comment_id}, {'$inc': {'likes': 1}})
    return jsonify({'message': 'Like added successfully'}), 200



@app.route("/comments", methods=["GET", "POST"])
def comments():
    if request.method == "POST":
        if 'image' in request.files:
            image = request.files['image']
            image_url = save_image(image)  # Save the image and get the URL
        else:
            image_url = None
        
        user_name = request.form['user_name']
        print(user_name)
        user = db.user.find_one({'email': user_name})
        
        if user:
            user_name = user.get('name', 'User')  # Provide a default value if 'name' is not present
        else:
            user_name = 'User'
        print(user_name)
        comment_data = {
            'user_name': user_name,
            'text': request.form['text'],
            'image_url': image_url,
            'likes': 0,
            'replies': []
        }
        
        db.comments.insert_one(comment_data)
        return jsonify({'message': 'Comment added successfully'}), 200
    
    elif request.method == "GET":
        comments = list(db.comments.find({}))
        comments = convert_object_id(comments)
        return jsonify(comments), 200

@app.route("/reply", methods=["POST"])
def reply():
    if 'image' in request.files:
        image = request.files['image']
        image_url = save_image(image)  # Save the image and get the URL
    else:
        image_url = None
    
    user_name = request.form['user_name']
    user = db.user.find_one({'email': user_name})
    if user:
            user_name = user.get('name', 'User')  # Provide a default value if 'name' is not present
    else:
            user_name = 'User'
    # user_name = user.get('name', 'User')
    
    reply_data = {
        'user_name': user_name,
        'text': request.form['text'],
        'image_url': image_url,
        'likes': 0
    }
    
    comment_id = ObjectId(request.form['comment_id'])
    db.comments.update_one({'_id': comment_id}, {'$push': {'replies': reply_data}})
    return jsonify({'message': 'Reply added successfully'}), 200


# @app.route("/send_message", methods=["POST"])
# def send_message():
#     data = request.form
#     channel_name = data['channel_name']
#     user_email = data['user_email']
#     message = data['message']
#     print(data)
#     user = db.user.find_one({'email': user_email})
#     if user:
#         user_name = user.get('name', user_email)
#         message_data = {
#             'channel_name': channel_name,
#             'user_name': user_name,
#             'message': message,
#             'timestamp': datetime.datetime.utcnow()
#         }
        
#         if 'image' in request.files:
#             image = request.files['image']
#             message_data['image_url'] = save_image(image)
        
#         result = db.messages.insert_one(message_data)
#         message_data['_id'] = str(result.inserted_id)  # Convert ObjectId to string
        
#         return jsonify({'message': 'Message sent successfully', 'message_data': message_data}), 200
    
#     return jsonify({'message': 'User not found'}), 404

@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.form
    channel_name = data['channel_name']
    user_email = data['user_email']
    message = data['message']
    # print(data)
    user = db.user.find_one({'email': user_email})
    if user:
        user_name = user.get('name', user_email)
        message_data = {
            'channel_name': channel_name,
            'user_name': user_name,
            'user_email': user_email,  # Include user email
            'message': message,
            'timestamp': datetime.datetime.utcnow()
        }
        
        if 'image' in request.files:
            image = request.files['image']
            message_data['image_url'] = save_image(image)
        
        result = db.messages.insert_one(message_data)
        message_data['_id'] = str(result.inserted_id)  # Convert ObjectId to string
        
        return jsonify({'message': 'Message sent successfully', 'message_data': message_data}), 200
    
    return jsonify({'message': 'User not found'}), 404

@app.route("/get_messages/<channel_name>", methods=["GET"])
def get_messages(channel_name):
    messages = list(db.messages.find({'channel_name': channel_name}).sort('timestamp'))
    for message in messages:
        message['_id'] = str(message['_id'])
    print(messages)
    return jsonify(messages), 200

if __name__ == '__main__':
    app.run(debug=True)

