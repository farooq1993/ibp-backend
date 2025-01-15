from flask import Blueprint, request, jsonify
import logging
from models.users import User, bcrypt
from utils.jwt import generate_token
from utils.db_setup import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

userlogin = Blueprint('user_login', __name__, url_prefix='/user')

@userlogin.route('/user_login', methods=['POST'])
def user_login():
    try:
        data = request.get_json()
        if not data:
            logger.warning("Invalid request format")
            return jsonify({'error': 'Invalid request format'}), 400

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            logger.warning("Email or password not provided")
            return jsonify({'error': 'Email and password are required'}), 400

        user = User.query.filter_by(email=email).first()

        if not user or not user.password:
            logger.warning(f"User not found or password missing for email: {email}")
            return jsonify({'error': 'Invalid email or password'}), 401

        if not user.check_password(password):
            logger.warning(f"Incorrect password for email: {email}")
            return jsonify({'error': 'Invalid email or password'}), 401

        token = generate_token(user.email)
        logger.info(f"User {email} logged in successfully")
        return jsonify({
            'message': 'Login successful',
            'user': {'id': user.id, 'email': user.email},
            'token': token
        }), 200

    except Exception as e:
        logger.error(f"An error occurred during login: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred. Please try again later.'}), 500