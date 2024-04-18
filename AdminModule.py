from flask import Blueprint, request, jsonify
from models import *

#________________________________________________________________________________________


admin_bp=Blueprint('admin',__name__)

#_________________________________________________________________________________________

@admin_bp.route('/view_hospitals', methods=['GET'])
def view_hospitals():
    try:
        hospitals = H_INFO.query.all()

        hospitals_data = []
        for hospital in hospitals:
            hospitals_data.append({
                'mail': hospital.MAIL,
                'h_name': hospital.H_NAME,
                'city': hospital.CITY,
                'address': hospital.ADDRESS,
                'contact': hospital.CONTACT
            })

        return jsonify({'status': 'success', 'hospitals': hospitals_data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error fetching hospitals: {str(e)}'}), 500
    
#____________________________________________________________________________________________________________________________________________________________________________
    

@admin_bp.route('/update_hospital/<hospital_mail>', methods=['POST'])
def update_hospital(hospital_mail):
    data = request.get_json(force=True)
    new_h_name = data.get('new_h_name')
    new_city = data.get('new_city')
    new_address = data.get('new_address')
    new_contact = data.get('new_contact')

    try:
        hospital = H_INFO.query.get(hospital_mail)
        if hospital:
            if new_h_name:
                hospital.H_NAME = new_h_name
            if new_city:
                hospital.CITY = new_city
            if new_address:
                hospital.ADDRESS = new_address
            if new_contact:
                hospital.CONTACT = new_contact

            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Hospital details updated successfully'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Hospital not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Error updating hospital: {str(e)}'}), 400
    
#______________________________________________________________________________________________________________________________________________________________
    
@admin_bp.route('/delete_hospital/<hospital_mail>', methods=['DELETE'])
def delete_hospital(hospital_mail):
    try:
        hospital = H_INFO.query.get(hospital_mail)
        if hospital:
            db.session.delete(hospital)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Hospital deleted successfully'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Hospital not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Error deleting hospital: {str(e)}'}), 500
    
#______________________________________________________________________________________________________________________________________________________________________________

@admin_bp.route('/view_parents', methods=['GET'])
def view_parents():
    try:
        parents = P_INFO.query.all()

        parents_data = []
        for parent in parents:
            parent_data = {
                'mail': parent.MAIL,
                'p_name': parent.P_NAME,
                'address': parent.ADDRESS,
                'contact': parent.CONTACT,
                'children': []  
            }

            children = C_INFO.query.filter_by(P_MAIL=parent.MAIL).all()
            for child in children:
                parent_data['children'].append({
                    'child_id': child.C_ID,
                    'c_name': child.C_NAME,
                    'age': child.AGE,
                    'dob': str(child.DOB),
                    'gender': child.GENDER,
                    'blood_type': child.BLOOD_TYPE
                })

            parents_data.append(parent_data)

        return jsonify({'status': 'success', 'parents': parents_data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error fetching parents: {str(e)}'}), 500
#_________________________________________________________

@admin_bp.route('/view_hospital/<h_mail>', methods=['GET'])
def view_hospital(h_mail):
    try:
        hospital = H_INFO.query.filter_by(MAIL=h_mail).first()

        if hospital:
            hospital_details = {
                'mail': hospital.MAIL,
                'h_name': hospital.H_NAME,
                'city': hospital.CITY,
                'address': hospital.ADDRESS,
                'contact': hospital.CONTACT
            }

            return jsonify({'status': 'success', 'hospital_details': hospital_details}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Hospital not found'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error fetching hospital details: {str(e)}'}), 500

#_______________________________________________________________________________________________________________________________________
    
@admin_bp.route('/view_children', methods=['GET'])
def view_children():
    try:
        children = C_INFO.query.all()

        children_data = []
        for child in children:
            p_mail = child.P_MAIL

            child_data = {
                'child_id': child.C_ID,
                'p_mail': p_mail,
                'c_name': child.C_NAME,
                'age': child.AGE,
                'dob': str(child.DOB),
                'gender': child.GENDER,
                'blood_type': child.BLOOD_TYPE
            }

            children_data.append(child_data)

        return jsonify({'status': 'success', 'children': children_data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error fetching children: {str(e)}'}), 500
    
#_______________________________________________________________________________________________________

#view all appointments

@admin_bp.route('/view_all_appointments', methods=['GET'])
def view_all_appointments():
    appointments = APPOINTMENT.query.all()
    
    appointment_list = []
    for appointment in appointments:
        parent_mail = C_INFO.query.filter_by(C_ID=appointment.C_ID).first().P_MAIL
        child_name = C_INFO.query.filter_by(C_ID=appointment.C_ID).first().C_NAME
        
        appointment_data = {
            'parent_mail': parent_mail,
            'child_name': child_name,
            'appointment_id': appointment.AP_ID,
            'vaccine': appointment.V_NAME,
            'status': appointment.STATUS,
            'hospital_name': appointment.H_NAME,
            'date_of_slot': appointment.DATE.strftime('%Y-%m-%d')
        }
        appointment_list.append(appointment_data)
    
    return jsonify({'appointments': appointment_list})