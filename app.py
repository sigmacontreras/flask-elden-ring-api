import os
import random
import sys
from flask import Flask, jsonify, send_from_directory, session, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)

# Dummy user data
users = {
    "armando.paredes@gmail.com": "123",
    "aquiles.bailo@gmail.com": "123",
    "esteban.quito": "123"
}
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/api/v1/allgreatswords')
def get_all_greatswords():
    img_dir = os.path.join(app.static_folder, 'img')
    greatswords = []

    for filename in os.listdir(img_dir):
        if filename.endswith('.png'):
            name = os.path.splitext(filename)[0]
            url = f'/static/img/{filename}'
            _id = round(random.uniform(1000, 10000), 2)  # Generate a random float ID
            greatswords.append({"url": "http://localhost:5000/api/v1" + url, "name": name, "id": _id})

    return jsonify(greatswords)


@app.route('/api/v1/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    try:
        print('before data', file=sys.stdout)
        data = request.get_json()
        print('Received data:', data)  # Debug statement to print received data
        if not data:
            return jsonify({"isAuthenticated": False, "isAuthorized": False, "error": "Invalid JSON data"}), 400
        username = data.get('email')
        password = data.get('password')
        if not username or not password:
            return jsonify(
                {"isAuthenticated": False, "isAuthorized": False, "error": "Missing username or password"}), 400
        if username in users and users[username] == password:
            session['username'] = username
            return jsonify({"isAuthenticated": True, "isAuthorized": True})
        else:
            return jsonify({"isAuthenticated": False, "isAuthorized": False})
    except Exception as e:
        print('Error:', str(e), file=sys.stderr)
        return jsonify({"isAuthenticated": False, "isAuthorized": False, "error": "An error occurred"}), 500


# Route to serve the static images directly
@app.route('/api/v1/static/img/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(app.static_folder, 'img'), filename)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
