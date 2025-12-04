from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from bson import ObjectId

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    user_id = get_jwt_identity()
    from app import db
    
    profile = db.patient_profiles.find_one({'userId': user_id})
    
    return jsonify({
        'wellnessGoals': profile.get('wellnessGoals', {}),
        'appointments': profile.get('appointments', []),
        'healthTip': "Drink 8 glasses of water daily!"
    }), 200

@patients_bp.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def manage_profile():
    user_id = get_jwt_identity()
    from app import db
    
    if request.method == 'GET':
        profile = db.patient_profiles.find_one({'userId': user_id})
        return jsonify(profile), 200
    
    elif request.method == 'PUT':
        data = request.json
        db.patient_profiles.update_one(
            {'userId': user_id},
            {'$set': data},
            upsert=True
        )
        return jsonify({'message': 'Profile updated'}), 200
