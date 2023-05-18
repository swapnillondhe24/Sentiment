from flask_cors import CORS
import jwt
from Scraper.reviews import generate_data

from Model.sentiment import generate_sentiment, scrape_amazon_product



import os
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson import ObjectId
from datetime import datetime, timedelta
load_dotenv()

app = Flask(__name__)
# app.use_x_sendfile = True

# Set maximum file size for uploads to 16 megabytes
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = "./"



cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
cors = CORS(app, resources={r"/*": {"origins": "*"}})
cors = CORS(app)


uri = os.getenv("MONGO_URI")
secret = os.getenv("SECRET_KEY")

client = MongoClient(uri)
db = client['DecenDS']
users = db['DecenDS_users']
app.config['SECRET_KEY'] = secret


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # print(request.headers)
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[0]

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = users.find_one({'_id': ObjectId(data['user_id'])})
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated



@app.route('/register', methods=['POST'])
def register():
    
    data = request.get_json()
    # print(data)
    if users.find_one({'username': data['username']}):
        return jsonify({'message': 'Username already exists'}), 409
    
    hashed_password = generate_password_hash(data['password'], method='sha256')
    user = {'username': data['username'], 'password': hashed_password,'email': data['email']}
    users.insert_one(user)
    return jsonify({'message': 'User registered successfully'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # print(data)
    user = users.find_one({'username': data['username']})
    if not user or not check_password_hash(user['password'], data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401
    # Generate JWT token
    payload = {
        'user_id': str(user['_id']),
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token})





@app.route('/image', methods=['GET'])
def get_images():
    images = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith('.png') and os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            images.append(filename)
    return {'images': images}

@app.route('/images/<path:filename>', methods=['GET'])
@token_required
def download_file(current_user,filename):
    return send_from_directory("../", filename, mimetype='image/png')


@app.route('/images', methods=['POST',])
@token_required
def get_image(current_user):
    print(request.json)
    filename = request.json['filename']
    print(filename)
    return send_from_directory("../", filename,mimetype='image/png')


@app.route('/productdetails', methods=['POST'])
@token_required
def get_details(current_user):
    url = request.json['url']
    return scrape_amazon_product(url)


@app.route('/sentiment', methods=['POST'])
@token_required
def get_sentiment(current_user):
    url = request.json['url']

    generate_data(url)

    print("Generating sentiment")
    ret = generate_sentiment()
    # print(ret)
    return jsonify(ret)


if __name__ == '__main__':

    app.run(port=5010)
