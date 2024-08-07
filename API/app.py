from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timezone
import logging
from logging.handlers import RotatingFileHandler
from sqlalchemy.exc import IntegrityError
from functools import wraps
from models import db, bcrypt, User, ClientDetails, Contract, Feedback, Meeting, EmployeeDetails, Note

app = Flask(__name__)

# Update your database connection here with the correct username and password
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Success786!!@localhost/pinkpearldecor_1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a random secret key

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

# Set up logging
if not app.debug:
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already taken, please choose another one'}), 409
    new_user = User(username=data['username'], role=data['role'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    
    if data['role'] == 'client':
        client_details = ClientDetails(
            user_id=new_user.user_id,
            name=data.get('name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            address=data.get('address', ''),
            initial_contact=data.get('initial_contact', ''),
            point_of_contact=data.get('point_of_contact', '')
        )
        db.session.add(client_details)
    elif data['role'] == 'admin':
        employee_details = EmployeeDetails(
            user_id=new_user.user_id,
            name=data.get('name', ''),
            role=data['role'],
            permissions=data.get('permissions', '')
        )
        db.session.add(employee_details)
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Error creating user details, please try again'}), 500
    return jsonify({'message': 'New user registered!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity={'user_id': user.user_id, 'role': user.role})
        return jsonify(access_token=access_token)
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        app.logger.debug(f'Current user: {current_user}')  # Debug statement
        if 'role' not in current_user or current_user['role'] != 'admin':
            return jsonify({'message': 'Admins only!'}), 403
        return fn(*args, **kwargs)
    return wrapper

@app.route('/clients/<int:client_id>/add_note', methods=['POST'])
@admin_required
def add_note_to_client(client_id):
    current_user = get_jwt_identity()
    data = request.get_json()
    client = ClientDetails.query.filter_by(id=client_id).first()
    if not client:
        return jsonify({'message': 'Client not found'}), 404
    
    note = Note(
        client_id=client.id,
        employee_id=current_user['user_id'],
        note=data['note']
    )
    client.updated_at = datetime.now(timezone.utc)
    
    db.session.add(note)
    db.session.commit()
    return jsonify({'message': 'Note added to client'})

@app.route('/clients/<int:client_id>/notes', methods=['GET'])
@jwt_required()
def get_client_notes(client_id):
    current_user = get_jwt_identity()
    client = ClientDetails.query.filter_by(id=client_id).first()
    if not client:
        return jsonify({'message': 'Client not found'}), 404

    notes = Note.query.filter_by(client_id=client_id).all()
    notes_list = [{'id': note.id, 'note': note.note, 'created_at': note.created_at, 'updated_at': note.updated_at, 'employee_id': note.employee_id} for note in notes]
    
    return jsonify({'notes': notes_list})

@app.route('/clients/<int:client_id>/report', methods=['GET'])
@admin_required
def generate_report(client_id):
    current_user = get_jwt_identity()
    client = ClientDetails.query.filter_by(id=client_id).first()
    if not client:
        return jsonify({'message': 'Client not found'}), 404
    
    contracts = Contract.query.filter_by(client_id=client_id).all()
    feedbacks = Feedback.query.filter_by(client_id=client_id).all()
    meetings = Meeting.query.filter_by(client_id=client_id).all()
    notes = Note.query.filter_by(client_id=client_id).all()
    
    report = {
        'client': {
            'name': client.name,
            'email': client.email,
            'phone': client.phone,
            'address': client.address,
            'initial_contact': client.initial_contact,
            'point_of_contact': client.point_of_contact
        },
        'contracts': [{'id': contract.id, 'details': contract.contract_details} for contract in contracts],
        'feedbacks': [{'id': feedback.id, 'feedback': feedback.feedback} for feedback in feedbacks],
        'meetings': [{'meeting_id': meeting.meeting_id, 'scheduled_at': meeting.scheduled_at, 'details': meeting.details,
        'employee_id': meeting.employee_id} for meeting in meetings],
        'notes': [{'id': note.id, 'note': note.note, 'created_at': note.created_at, 'updated_at': note.updated_at, 'employee_id': note.employee_id} for note in notes]
    }
    
    return jsonify(report)

@app.route('/clients/<int:client_id>/feedback', methods=['POST'])
@jwt_required()
def add_feedback_to_employee(client_id):
    current_user = get_jwt_identity()
    data = request.get_json()
    
    client = ClientDetails.query.filter_by(id=client_id, user_id=current_user['user_id']).first()
    if not client:
        return jsonify({'message': 'Client not found or unauthorized'}), 404
    
    feedback = Feedback(
        user_id=current_user['user_id'],
        client_id=client_id,
        feedback=data['feedback']
    )
    
    db.session.add(feedback)
    db.session.commit()
    return jsonify({'message': 'Feedback submitted'})

@app.route('/clients/<int:client_id>/feedbacks', methods=['GET'])
@jwt_required()
def get_client_feedbacks(client_id):
    client = ClientDetails.query.filter_by(id=client_id).first()
    if not client:
        return jsonify({'message': 'Client not found'}), 404

    feedbacks = Feedback.query.filter_by(client_id=client_id).all()
    feedback_list = [{'id': fb.id, 'feedback': fb.feedback, 'created_at': fb.created_at, 'updated_at': fb.updated_at} for fb in feedbacks]
    
    return jsonify({'feedbacks': feedback_list})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'message': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
