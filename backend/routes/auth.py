from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    
    # Hash password
    hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    user = {
        'email': data['email'],
        'password': hashed_pw,
        'role': data.get('role', 'patient'),
        'consentGiven': data.get('consent', False)
    }
    
    from app import db
    db.users.insert_one(user)
    
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    from app import db
    
    user = db.users.find_one({'email': data['email']})
    
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        token = create_access_token(
            identity=str(user['_id']),
            additional_claims={'role': user['role']},
            expires_delta=timedelta(hours=24)
        )
        return jsonify({'token': token, 'role': user['role']}), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401
