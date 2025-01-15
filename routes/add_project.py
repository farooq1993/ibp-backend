from flask import Blueprint, request, jsonify
import logging
from models.project import Project
from utils.db_setup import db
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


addproject = Blueprint('/project_add', __name__, url_prefix='/project_add')
@addproject.route('add_project', methods=['POST'])
def add_project():
    try:
        # Parse incoming JSON data
        data = request.get_json()

        # Log the incoming data
        logger.info("Project creation data: %s", data)

        # Validate data
        if not data:
            return jsonify({'error': 'Fields are required'}), 400

        required_fields = ['title', 'programs', 'directorate', 'technical_description', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400

        try:
            # Function to parse fiscal year format to datetime
            def parse_fiscal_year(fy_date):
                # Extract year from fiscal year format, e.g., FY2025/26 -> 2025
                year = int(fy_date[2:6])  # Skip "FY" and take the first four digits
                # Assume fiscal year starts on April 1
                return datetime(year, 4, 1)

            # Convert fiscal year strings to datetime
            start_date = parse_fiscal_year(data['start_date'])
            end_date = parse_fiscal_year(data['end_date'])

            # Adjust end_date to the fiscal year end (March 31 of the following year)
            end_date = datetime(end_date.year + 1, 3, 31)

            # Calculate duration in days
            duration = (end_date - start_date).days

            # Add parsed dates and duration to the data
            data['start_date'] = start_date
            data['end_date'] = end_date
            data['duration'] = duration
        except ValueError as ve:
            logger.error("Date parsing error: %s", ve, exc_info=True)
            return jsonify({'error': 'Invalid fiscal year format. Use FY2025/26 format.'}), 400

        # Create a new project instance
        new_project = Project(**data)

        # Add to the database session and commit
        db.session.add(new_project)
        db.session.commit()

        # Log success
        logger.info("Project saved successfully with ID: %s", new_project.id)

        return jsonify({'msg': 'Project added successfully', 'project_id': new_project.id}), 201

    except Exception as e:
        # Log the exception
        logger.error("Error adding project: %s", e, exc_info=True)
        return jsonify({'error': 'An error occurred while saving the project'}), 500