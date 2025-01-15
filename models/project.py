from utils.db_setup import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    programs = db.Column(db.String(300), nullable=False)
    directorate = db.Column(db.String(300), nullable=False)
    technical_description = db.Column(db.String(300), nullable=False)
    start_date = db.Column(db.DateTime,nullable=False)
    duration = db.Column(db.Integer(), nullable=False)
    end_date =  db.Column(db.DateTime,nullable=False)
    
    
    
    
    