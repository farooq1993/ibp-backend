from flask_sqlalchemy import SQLAlchemy

# Single SQLAlchemy instance
db = SQLAlchemy()

def init_db(app):
    """
    Initialize the database with the given Flask app.
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
