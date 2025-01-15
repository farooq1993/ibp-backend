from flask import Blueprint, request, jsonify
from models.myc import MultiYearCommitment
from datetime import datetime
from utils.db_setup import db

myc = Blueprint('/add_myc', __name__, url_prefix='/add_myc')



@myc.route('/multi_year_commitment', methods=['POST'])
def add_mycommitment():
    try:
        data = request.get_json()

        new_commitment = MultiYearCommitment(
            financing_agreement_title=data['financing_agreement_title'],
            annual_appropriations=data.get('annual_appropriations'),
            approved_payments=data.get('approved_payments'),
            arrears=data.get('arrears'),
            verified_arrears=data.get('verified_arrears'),
            unverified_arrears=data.get('unverified_arrears'),
            arrears_payment=data.get('arrears_payment'),
            arrears_6_months_plus=data.get('arrears_6_months_plus'),
            contract_reference_number=data.get('contract_reference_number'),
            contract_expenditures=data.get('contract_expenditures'),
            contract_implementation_plan=data.get('contract_implementation_plan'),
            contract_name=data['contract_name'],
            contractor_name=data.get('contractor_name'),
            contract_start_date=datetime.strptime(data.get('contract_start_date'), '%Y-%m-%d') if data.get('contract_start_date') else None,
            contract_end_date=datetime.strptime(data.get('contract_end_date'), '%Y-%m-%d') if data.get('contract_end_date') else None,
            contract_payment_plan=data.get('contract_payment_plan'),
            contract_status=data.get('contract_status'),
            contract_terms=data.get('contract_terms'),
            contract_value=data.get('contract_value'),
            counterpart_requirement_specification=data.get('counterpart_requirement_specification'),
            counterpart_value=data.get('counterpart_value'),
            currency=data.get('currency'),
            counterpart_financing_plan=data.get('counterpart_financing_plan'),
            funding_source=data.get('funding_source'),
            fy_1_myc=data.get('fy_1_myc'),
            mtef_ceilings=data.get('mtef_ceilings'),
            non_contractual_commitments=data.get('non_contractual_commitments'),
            programme_code=data.get('programme_code'),
            programme_name=data.get('programme_name'),
            project_classification=data.get('project_classification'),
            project_code=data.get('project_code'),
            project_end_date=datetime.strptime(data.get('project_end_date'), '%Y-%m-%d') if data.get('project_end_date') else None,
            project_name=data.get('project_name'),
            project_start_date=datetime.strptime(data.get('project_start_date'), '%Y-%m-%d') if data.get('project_start_date') else None,
            vote_code=data.get('vote_code'),
            vote_name=data.get('vote_name')
        )

        db.session.add(new_commitment)
        db.session.commit()

        return jsonify({'message': 'Multi-Year Commitment added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
# GET: Retrieve all multi-year commitments or a specific one by ID
@myc.route('/multi_year_commitment', methods=['GET'])
def get_commitments():
    commitment_id = request.args.get('id')  # Optional query parameter
    if commitment_id:
        commitment = MultiYearCommitment.query.get(commitment_id)
        if not commitment:
            return jsonify({'error': 'Commitment not found'}), 404
        return jsonify(commitment.to_dict()), 200
    else:
        commitments = MultiYearCommitment.query.all()
        return jsonify([c.to_dict() for c in commitments]), 200


# PATCH: Update specific fields of a commitment
@myc.route('/multi_year_commitment/<int:id>', methods=['PATCH'])
def patch_commitment(id):
    commitment = MultiYearCommitment.query.get(id)
    if not commitment:
        return jsonify({'error': 'Commitment not found'}), 404

    data = request.get_json()
    for key, value in data.items():
        if hasattr(commitment, key):
            setattr(commitment, key, value)

    db.session.commit()
    return jsonify({'message': 'Commitment updated successfully', 'commitment': commitment.to_dict()}), 200


# PUT: Replace a commitment completely
@myc.route('/multi_year_commitment/<int:id>', methods=['PUT'])
def put_commitment(id):
    commitment = MultiYearCommitment.query.get(id)
    if not commitment:
        return jsonify({'error': 'Commitment not found'}), 404

    data = request.get_json()

    # Update all fields (ensure validation in production code)
    commitment.financing_agreement_title = data.get('financing_agreement_title')
    commitment.annual_appropriations = data.get('annual_appropriations')
    commitment.approved_payments = data.get('approved_payments')
    commitment.arrears = data.get('arrears')
    # Continue for all fields...

    db.session.commit()
    return jsonify({'message': 'Commitment replaced successfully', 'commitment': commitment.to_dict()}), 200


# DELETE: Remove a commitment
@myc.route('/multi_year_commitment/<int:id>', methods=['DELETE'])
def delete_commitment(id):
    commitment = MultiYearCommitment.query.get(id)
    if not commitment:
        return jsonify({'error': 'Commitment not found'}), 404

    db.session.delete(commitment)
    db.session.commit()
    return jsonify({'message': 'Commitment deleted successfully'}), 200
