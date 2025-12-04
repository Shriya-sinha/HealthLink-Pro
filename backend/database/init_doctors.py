"""
Initialize MongoDB with sample doctor data
Run this script to populate doctors in the database
"""
import os
import sys
from pathlib import Path
from datetime import datetime
import bcrypt

# Add parent directory to path so healthcare module can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare.settings')

import django
django.setup()

from api.models import User, ProviderProfile

# Sample doctors data
DOCTORS_DATA = [
    {
        'email': 'dr.smith@hospital.com',
        'password': 'SecurePass123!',
        'specialty': 'Cardiology',
        'license_number': 'LIC001',
        'qualifications': ['MD from Harvard Medical School', 'Board Certified Cardiologist'],
        'experience_years': '15',
        'clinic_address': '123 Medical Plaza, Suite 100, New York, NY 10001',
        'phone': '+1-555-0101',
    },
    {
        'email': 'dr.johnson@hospital.com',
        'password': 'SecurePass123!',
        'specialty': 'Pediatrics',
        'license_number': 'LIC002',
        'qualifications': ['MD from Johns Hopkins', 'Board Certified Pediatrician'],
        'experience_years': '12',
        'clinic_address': '456 Healthcare Blvd, Suite 200, Boston, MA 02101',
        'phone': '+1-555-0102',
    },
    {
        'email': 'dr.williams@hospital.com',
        'password': 'SecurePass123!',
        'specialty': 'Neurology',
        'license_number': 'LIC003',
        'qualifications': ['MD from Stanford', 'Neurology Specialist'],
        'experience_years': '18',
        'clinic_address': '789 Wellness Center, Suite 300, San Francisco, CA 94102',
        'phone': '+1-555-0103',
    },
    {
        'email': 'dr.brown@hospital.com',
        'password': 'SecurePass123!',
        'specialty': 'Orthopedics',
        'license_number': 'LIC004',
        'qualifications': ['MD from Mayo Clinic', 'Orthopedic Surgeon'],
        'experience_years': '20',
        'clinic_address': '321 Medical Center, Suite 400, Los Angeles, CA 90001',
        'phone': '+1-555-0104',
    },
    {
        'email': 'dr.garcia@hospital.com',
        'password': 'SecurePass123!',
        'specialty': 'Dermatology',
        'license_number': 'LIC005',
        'qualifications': ['MD from UCLA', 'Board Certified Dermatologist'],
        'experience_years': '10',
        'clinic_address': '654 Health Plaza, Suite 500, Chicago, IL 60601',
        'phone': '+1-555-0105',
    },
]


def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')


def init_doctors():
    """Initialize doctors in database"""
    print('Initializing doctors...')
    
    for doctor_data in DOCTORS_DATA:
        email = doctor_data['email']
        
        # Check if doctor already exists
        existing_user = User.objects(email=email).first()
        if existing_user:
            print(f'Doctor {email} already exists, skipping...')
            continue
        
        try:
            # Create user account for doctor
            user = User(
                email=email,
                password_hash=hash_password(doctor_data['password']),
                role='provider',
                consent_given=True,
                is_active=True,
            )
            user.save()
            
            # Create provider profile
            provider = ProviderProfile(
                user_id=str(user.id),
                specialty=doctor_data['specialty'],
                license_number=doctor_data['license_number'],
                qualifications=doctor_data['qualifications'],
                experience_years=doctor_data['experience_years'],
                clinic_address=doctor_data['clinic_address'],
                phone=doctor_data['phone'],
                available_hours={
                    'Monday': '09:00-17:00',
                    'Tuesday': '09:00-17:00',
                    'Wednesday': '09:00-17:00',
                    'Thursday': '09:00-17:00',
                    'Friday': '09:00-17:00',
                    'Saturday': '10:00-14:00',
                },
                patients=[],
            )
            provider.save()
            
            print(f'✓ Created doctor: {email} ({doctor_data["specialty"]})')
        
        except Exception as e:
            print(f'✗ Failed to create doctor {email}: {str(e)}')


if __name__ == '__main__':
    try:
        init_doctors()
        print('\n✓ Doctor initialization completed!')
    except Exception as e:
        print(f'\n✗ Error during initialization: {str(e)}')
        sys.exit(1)
