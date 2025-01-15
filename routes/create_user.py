from flask import Blueprint, request, jsonify
import logging
from models.users import User
from utils.db_setup import db
from models.users import User, bcrypt


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


createuser = Blueprint('create_user', __name__, url_prefix='/user')

@createuser.route('/create_user', methods=['POST'])
def create_user():
    try:
        # Get JSON data from request
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Log the password before hashing for debugging
        logger.debug(f"Password before hashing: {password}")

        logger.debug(f"Hashed password: {password}")

        # Proceed with user creation
        new_user = User(username=username, email=email, password=password)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        logger.info("User created successfully: %s", username)
        return jsonify({'msg': 'User created successfully'}), 201

    except Exception as e:
        logger.error("Error creating user: %s", str(e))
        return jsonify({'error': 'Unable to create user!'}), 500
    

@createuser.route('/getuser', methods=['GET'])
def get_all_user():
    users = User.query.all()
    return jsonify({'msg':"all data"})