import jwt
from flask import jsonify,request
from datetime import datetime, timedelta
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY=os.getenv('SECRET_KEY')


def generate_token(email):
    """
    Generate a JWT token for the user with a 60-minute expiration time.
    """
    payload = {
        'email': email,
        'exp': datetime.now() + timedelta(minutes=60),
        'iat': datetime.now()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Decorator for login-required routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        try:
            # Decode and verify token
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user_id = decoded_token['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 401
        return f(*args, **kwargs)
    return decorated_function