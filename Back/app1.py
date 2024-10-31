import os
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from database import db

# Initialize Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True,resources={r"/api/*": {"origins": "http://192.168.0.161:8081"}})

# Set up the base directory and the database URI
base_dir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'library.db')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

# Bind the SQLAlchemy object to the app
db.init_app(app)

# Initialize JWTManager with the app
jwt = JWTManager(app)

# Import models here to ensure they are known to SQLAlchemy
with app.app_context():
    from models import User
    db.create_all()

# Define the login route
@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
   
      

    # Normal POST request handling for login
    #data = request.form
   
    #username = data.get('username')
    #password = data.get('password')
    data = request.get_json()
    username = data['param1']
    password = data['param2']

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Generate token using the instance method 'generate_auth_token'
        token = user.generate_auth_token(jwt)
        return jsonify({'message': 'Login Successful', 'token': token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
