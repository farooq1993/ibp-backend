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


# Get project by ID
@addproject.route('/getProjectById/<int:id>/', methods=['GET'])
def getSingleProject(id):
    single_project = Project.query.get(id)  # Fetch the project by primary key

    if not single_project:
        return jsonify({'error': 'Project not found'}), 404

    project_data = {
        'id': single_project.id,
        'title': single_project.title,
        'programs': single_project.programs,
        'directorate': single_project.directorate,
        'technical_description': single_project.technical_description,
        'start_date': single_project.start_date.strftime('%Y-%m-%d') if single_project.start_date else None,
        'duration': single_project.duration,
        'end_date': single_project.end_date.strftime('%Y-%m-%d') if single_project.end_date else None,
        'status': single_project.status.value if single_project.status else "NOT SET",
        'code': single_project.code,
    }

    return jsonify({'data': project_data}), 200


@addproject.route('/updateProject/<int:id>/', methods=['PUT'])
def updateProject(id):
    # Fetch the project by ID
    project = Project.query.get(id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    # Parse JSON data from the request
    data = request.json

    # Update fields if they are provided in the request
    if 'title' in data:
        project.title = data['title']
    if 'programs' in data:
        project.programs = data['programs']
    if 'directorate' in data:
        project.directorate = data['directorate']
    if 'technical_description' in data:
        project.technical_description = data['technical_description']
    if 'start_date' in data:
        project.start_date = data['start_date']  # Ensure the date format matches your model
    if 'duration' in data:
        project.duration = data['duration']
    if 'end_date' in data:
        project.end_date = data['end_date']  # Ensure the date format matches your model
    if 'status' in data:
        try:
            # Convert the status to the Enum type
            project.status = ProjectStatus[data['status']]
        except KeyError:
            return jsonify({'error': 'Invalid status value'}), 400
    if 'code' in data:
        project.code = data['code']

    # Commit the changes to the database
    try:
        db.session.commit()
        return jsonify({'message': 'Project updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

