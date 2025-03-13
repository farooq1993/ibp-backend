from utils.db_setup import db
from models.project import Project
# class MultiYearCommitment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     financing_agreement_title = db.Column(db.String(255), nullable=False)
#     annual_appropriations = db.Column(db.Float, nullable=True)
#     approved_payments = db.Column(db.Float, nullable=True)
#     arrears = db.Column(db.Float, nullable=True)
#     verified_arrears = db.Column(db.Float, nullable=True)
#     unverified_arrears = db.Column(db.Float, nullable=True)
#     arrears_payment = db.Column(db.Float, nullable=True)
#     arrears_6_months_plus = db.Column(db.Float, nullable=True)
#     contract_reference_number = db.Column(db.String(255), nullable=True)
#     contract_expenditures = db.Column(db.Float, nullable=True)
#     contract_implementation_plan = db.Column(db.Text, nullable=True)
#     contract_name = db.Column(db.String(255), nullable=False)
#     contractor_name = db.Column(db.String(255), nullable=True)
#     contract_start_date = db.Column(db.Date, nullable=True)
#     contract_end_date = db.Column(db.Date, nullable=True)
#     contract_payment_plan = db.Column(db.Text, nullable=True)
#     contract_status = db.Column(db.String(100), nullable=True)
#     contract_terms = db.Column(db.Text, nullable=True)
#     contract_value = db.Column(db.Float, nullable=True)
#     counterpart_requirement_specification = db.Column(db.Text, nullable=True)
#     counterpart_value = db.Column(db.Float, nullable=True)
#     currency = db.Column(db.String(50), nullable=True)
#     counterpart_financing_plan = db.Column(db.Text, nullable=True)
#     funding_source = db.Column(db.String(100), nullable=True)
#     fy_1_myc = db.Column(db.Float, nullable=True)
#     mtef_ceilings = db.Column(db.Float, nullable=True)
#     non_contractual_commitments = db.Column(db.Text, nullable=True)
#     programme_code = db.Column(db.String(50), nullable=True)
#     programme_name = db.Column(db.String(255), nullable=True)
#     project_classification = db.Column(db.String(100), nullable=True)
#     project_code = db.Column(db.String(50), nullable=True)
#     project_end_date = db.Column(db.Date, nullable=True)
#     project_name = db.Column(db.String(255), nullable=True)
#     project_start_date = db.Column(db.Date, nullable=True)
#     vote_code = db.Column(db.String(50), nullable=True)
#     vote_name = db.Column(db.String(255), nullable=True)
#         # Foreign Key for Project
#     project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
#     # Define Relationship
#     project = db.relationship(Project, back_populates='commitments')
class MultiYearCommitment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    financing_agreement_title = db.Column(db.String(255), nullable=False)
    annual_appropriations = db.Column(db.Float, nullable=True)
    approved_payments = db.Column(db.Float, nullable=True)
    arrears = db.Column(db.Float, nullable=True)
    verified_arrears = db.Column(db.Float, nullable=True)
    unverified_arrears = db.Column(db.Float, nullable=True)
    arrears_payment = db.Column(db.Float, nullable=True)
    arrears_6_months_plus = db.Column(db.Float, nullable=True)
    contract_reference_number = db.Column(db.String(255), nullable=True)
    contract_expenditures = db.Column(db.Float, nullable=True)
    contract_implementation_plan = db.Column(db.Text, nullable=True)
    contract_name = db.Column(db.String(255), nullable=False)
    contractor_name = db.Column(db.String(255), nullable=True)
    contract_start_date = db.Column(db.Date, nullable=True)
    contract_end_date = db.Column(db.Date, nullable=True)
    contract_payment_plan = db.Column(db.Text, nullable=True)
    contract_status = db.Column(db.String(100), nullable=True)
    contract_terms = db.Column(db.Text, nullable=True)
    contract_value = db.Column(db.Float, nullable=True)
    counterpart_requirement_specification = db.Column(db.Text, nullable=True)
    counterpart_value = db.Column(db.Float, nullable=True)
    currency = db.Column(db.String(50), nullable=True)
    counterpart_financing_plan = db.Column(db.Text, nullable=True)
    funding_source = db.Column(db.String(100), nullable=True)
    fy_1_myc = db.Column(db.Float, nullable=True)
    mtef_ceilings = db.Column(db.Float, nullable=True)
    non_contractual_commitments = db.Column(db.Text, nullable=True)
    programme_code = db.Column(db.String(50), nullable=True)
    programme_name = db.Column(db.String(255), nullable=True)
    project_classification = db.Column(db.String(100), nullable=True)
    project_code = db.Column(db.String(50), nullable=True)
    project_end_date = db.Column(db.Date, nullable=True)
    project_name = db.Column(db.String(255), nullable=True)
    project_start_date = db.Column(db.Date, nullable=True)
    vote_code = db.Column(db.String(50), nullable=True)
    vote_name = db.Column(db.String(255), nullable=True)
    
    # New fields based on your list
    contract_value_external = db.Column(db.Float, nullable=True)  # Contract Value External (UGX)
    annual_penalty_interest_rate = db.Column(db.Float, nullable=True)  # Annual Penalty Interest Rate (%)
    balance_on_contract_value = db.Column(db.Float, nullable=True)  # Balance on Contract Value (UGX)
    cumulative_arrears_ending = db.Column(db.Float, nullable=True)  # Cumulative Arrears ending undefined (UGX)
    cumulative_arrears_penalty_exposure = db.Column(db.Float, nullable=True)  # Cumulative Arrears Penalty Exposure (UGX)
    procurement_ref_no = db.Column(db.String(255), nullable=True)  # Procurement Ref. No.
    description_of_procurement = db.Column(db.Text, nullable=True)  # Description of Procurement
    category_of_procurement = db.Column(db.String(255), nullable=True)  # Category of Procurement
    stage_of_procurement = db.Column(db.String(255), nullable=True)  # Stage of Procurement
    estimated_contract_value = db.Column(db.Float, nullable=True)  # Estimated Contract Value (UGX)
    source_of_financing = db.Column(db.String(255), nullable=True)  # Source of Financing
    estimated_commencement_date = db.Column(db.Date, nullable=True)  # Estimated Commencement Date
    estimated_contract_end_date = db.Column(db.Date, nullable=True)  # Estimated Contract End Date

    # Fiscal Year Fields (as Strings)
    fy2021_22 = db.Column(db.String(50), nullable=True)  # FY2021/22 (e.g., "2021/22")
    fy2022_23 = db.Column(db.String(50), nullable=True)  # FY2022/23 (e.g., "2022/23")
    fy2023_24 = db.Column(db.String(50), nullable=True)  # FY2023/24 (e.g., "2023/24")
    fy2024_25 = db.Column(db.String(50), nullable=True)  # FY2024/25 (e.g., "2024/25")
    fy2025_26 = db.Column(db.String(50), nullable=True)  # FY2025/26 (e.g., "2025/26")
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    # Define Relationship
    project = db.relationship('Project', back_populates='commitments')
    
    
    def to_dict(self):
        """Convert SQLAlchemy model to dictionary"""
        data = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        
        # Convert date fields to string format (YYYY-MM-DD)
        for key in ['contract_start_date', 'contract_end_date']:
            if data.get(key):
                data[key] = data[key].strftime('%Y-%m-%d')

        # Include Project Data
        if self.project:
            data['project'] = self.project.to_dict()

        return data