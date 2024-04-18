from flask import Blueprint, jsonify, session, request
from models import *

#_____________________________________________________________________________________________________________________________________________________________________________

hospital_bp = Blueprint('hospital', __name__)

#______________________________________________________________________________________________________________________________________________________________________________

@hospital_bp.route('/get_hospital_details', methods=['POST'])
def get_hospital_details():
    try:
        data=request.get_json()
     
        hospital_mail = data.get('hospital_mail')
        hospital = H_INFO.query.filter_by(MAIL=hospital_mail).first()


        if not hospital:
            return jsonify({'status': 'error', 'message': 'hospital not found'}), 404

        hospital_data = {
            'mail':hospital.MAIL,
            'h_name': hospital.H_NAME,
            'address': hospital.ADDRESS,
            'contact': hospital.CONTACT,
            'city':hospital.CITY
        }

        return jsonify({'status': 'success', 'hospital_details': hospital_data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error fetching hospital details: {str(e)}'}), 500
    
#___________________________________________________________________________________________________________________________________________
    
@hospital_bp.route('/view_appointments', methods=['POST'])
def view_hospital_appointments():
    try:
        data = request.get_json()
    
        hospital_mail = data.get("h_mail")
        hospital = H_INFO.query.filter_by(MAIL=hospital_mail).first()

        if not hospital:
            return jsonify({'status': 'error', 'message': 'Hospital not found'}), 404

        appointments = APPOINTMENT.query.filter_by(H_NAME=hospital.H_NAME).all()

        appointments_data = []
        for appointment in appointments:
            patient = C_INFO.query.get(appointment.C_ID)
            if patient:
                appointment_data = {
                    'ap_id': appointment.AP_ID,
                    'c_id': appointment.C_ID,
                    'c_name': patient.C_NAME,
                    'c_age': patient.AGE,
                    'h_name': appointment.H_NAME,
                    'a_date': str(appointment.DATE),
                    'v_name': appointment.V_NAME,
                    'status': appointment.STATUS
                }
                appointments_data.append(appointment_data)

        return jsonify({'status': 'success', 'appointments': appointments_data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error fetching hospital appointments: {str(e)}'}), 500

#__________________________________________________________________________________________________________________________________
    
@hospital_bp.route('/update_appointment_status/<ap_id>', methods=['POST'])
def update_appointment_status(ap_id):
    try:
        appointment = APPOINTMENT.query.get(ap_id)

        if not appointment:
            return jsonify({'status': 'error', 'message': 'Appointment not found'}), 404

        new_status = request.json.get('new_status')

        appointment.STATUS = new_status
        db.session.commit()

        return jsonify({'status': 'success', 'message': f'Appointment status updated to: {new_status}'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error updating appointment status: {str(e)}'}), 500
