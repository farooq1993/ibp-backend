from utils.db_setup import db
from flask_bcrypt import Bcrypt

# Initialize Bcrypt instance
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.hash_password(password)

    def hash_password(self, password):
        """Hash the password before storing."""
        if not isinstance(password, str) or not password:
            raise ValueError("Password must be a non-empty string")
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check if the provided password matches the hashed password."""
        if not password:
            return False
        return bcrypt.check_password_hash(self.password, password)
