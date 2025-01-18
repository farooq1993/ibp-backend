from flask import Blueprint, request, jsonify
import logging
from constant.project_status import ProjectStatus
from models.project import Project
from utils.db_setup import db
from datetime import datetime
from dateutil.relativedelta import relativedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


addproject = Blueprint('/project_add', __name__, url_prefix='/project_add')


@addproject.route('add_project', methods=['POST'])
def add_project():
    try:
        # Parse incoming JSON data
        data = request.get_json()

        logger.info("Project creation data: %s", data)

        if not data:
            return jsonify({'error': 'Fields are required'}), 400

        required_fields = ['title', 'programs', 'directorate', 'technical_description', 'start_date', 'duration_month']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400

        try:
            # Parse fiscal year format for start_date
            def parse_fiscal_year(fy_date):
                """Parse a fiscal year format (e.g., FY2025/26) to a datetime object."""
                year = int(fy_date[2:6])  # Extract the starting year
                return datetime(year, 4, 1)  # Fiscal year starts on April 1

            # Convert start_date from fiscal year to datetime
            start_date = parse_fiscal_year(data['start_date'])

            # Calculate end_date based on duration_month
            duration_month = int(data['duration_month'])
            end_date = start_date + relativedelta(months=duration_month)

            # Calculate duration in days
            duration = (end_date - start_date).days

            # Add parsed dates and duration to the data
            data['start_date'] = start_date
            data['end_date'] = end_date
            data['duration'] = duration
        except ValueError as ve:
            logger.error("Date parsing error: %s", ve, exc_info=True)
            return jsonify({'error': 'Invalid fiscal year format. Use FY2025/26 format.'}), 400

        # Generate project code
        data['code'] = Project.generate_code()

        # Create a new project instance
        new_project = Project(
            title=data['title'],
            programs=data['programs'],
            directorate=data['directorate'],
            technical_description=data['technical_description'],
            start_date=data['start_date'],
            duration=data['duration'],
            end_date=data['end_date'],
            code=data['code'],
            status=ProjectStatus.DRAFT  # Default to DRAFT
        )

        # Add to the database session and commit
        db.session.add(new_project)
        db.session.commit()

        logger.info("Project saved successfully with ID: %s", new_project.id)

        return jsonify({'msg': 'Project added successfully', 'project_id': new_project.id}), 201

    except Exception as e:
        logger.error("Error adding project: %s", e, exc_info=True)
        return jsonify({'error': 'An error occurred while saving the project'}), 500
    
    

@addproject.route('/getAllProject', methods=['GET'])
def getAllProjectList():
    projects = Project.query.all()  # Query all projects
    
    project_list = []
    for project in projects:
        project_data = {
            'id': project.id,
            'title': project.title,
            'programs': project.programs,
            'directorate': project.directorate,
            'technical_description': project.technical_description,
            'start_date': project.start_date.strftime('%Y-%m-%d') if project.start_date else None,
            'duration': project.duration,
            'end_date': project.end_date.strftime('%Y-%m-%d') if project.end_date else None,
            'status': project.status.value if project.status else "NOT SET",  # Handle NoneType for status
            'code': project.code,
        }
        project_list.append(project_data)

    return jsonify({'data': project_list}), 200
    
