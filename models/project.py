from utils.db_setup import db
from constant.project_status import ProjectStatus


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    programs = db.Column(db.String(300), nullable=False)
    directorate = db.Column(db.String(300), nullable=False)
    technical_description = db.Column(db.String(300), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer(), nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(ProjectStatus), default=ProjectStatus.DRAFT.value, nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)

    commitments = db.relationship('MultiYearCommitment', back_populates='project', cascade="all, delete-orphan")
    
    @staticmethod
    def generate_code():
        last_project = db.session.query(Project).order_by(Project.id.desc()).first()
        if last_project and last_project.code:
            new_code = str(int(last_project.code) + 1).zfill(4)
        else:
            new_code = '0001'  
        return new_code

    
    
    
    
    