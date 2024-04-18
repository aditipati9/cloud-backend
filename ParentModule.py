from flask import Blueprint, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from models import *
import datetime
import sqlalchemy.exc
#______________________________________________________________________________

parent_bp = Blueprint('parent', __name__)

#______________________________________________________________________________

@parent_bp.route('/add_child/<p_mail>', methods=['POST'])
def add_child(p_mail):
    # Parse JSON data from the request
    data = request.get_json()
    
    # Extract child's information from the data
    c_name = data.get('c_name')
    age = data.get('age')
    dob_str = data.get('dob')
    dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date()

    gender = data.get('gender')
    blood_type = data.get('blood_type')
    
    # Create a new instance of C_INFO with the extracted data
    try:
        parent = P_INFO.query.filter_by(MAIL=p_mail).first()
        print(parent)
        if parent is None:
            # Parent email does not exist, return an error response
            return jsonify({'error': 'Parent email does not exist'}), 400
        child = C_INFO(
        C_NAME=c_name,
        AGE=age,
        DOB=dob,
        GENDER=gender,
        BLOOD_TYPE=blood_type,
        P_MAIL=p_mail 
    )
    # Add the new child instance to the database session and commit the transaction
        db.session.add(child)
        db.session.commit()
    
    # Return a JSON response indicating success
        return jsonify({'status': 'success', 'child_id': child.C_ID}), 200
    #commments
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'User name already exist'}), 400

#________________________________________________________________________________________________________________

@parent_bp.route('/delete_child/<child_id>', methods=['DELETE'])
def delete_child(child_id):
    try:
        # Query the child by ID and delete it
        child = C_INFO.query.filter_by(C_ID=child_id).first()
        if child:
            db.session.delete(child)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Child deleted successfully'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Child not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Error deleting child: {str(e)}'}), 500

#___________________________________________________________________________________________________________________________

@parent_bp.route('/update_child/<p_mail>/<child_id>', methods=['POST'])
def update_child(p_mail, child_id):
    # Get the data from the request form
    data = request.get_json(force=True) 
    new_child_name = data.get('new_child_name')
    new_age = data.get('new_age')
    new_dob_str = data.get('new_dob')
    new_gender = data.get('new_gender')
    new_blood_type = data.get('new_blood_type')

    # Check if the parent exists
    parent = P_INFO.query.filter_by(MAIL=p_mail).first()
    if not parent:
        return jsonify({'status': 'error', 'message': 'Parent not found'}), 404

    # Check if the child exists
    child = C_INFO.query.filter_by(P_MAIL=p_mail, C_ID=child_id).first()
    if not child:
        return jsonify({'status': 'error', 'message': 'Child not found'}), 404

    try:
        # Update child's information
        if new_child_name:
            child.C_NAME = new_child_name
        if new_age:
            child.AGE = new_age  # Convert to integer
        if new_dob_str:
            new_dob = datetime.datetime.strptime(new_dob_str, '%Y-%m-%d').date()
            child.DOB = new_dob
        if new_gender:
            child.GENDER = new_gender
        if new_blood_type:
            child.BLOOD_TYPE = new_blood_type

        db.session.commit()

        # Return success message
        return jsonify({'status': 'success', 'message': 'Child information updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        # Return error message
        return jsonify({'status': 'error', 'message': f'Error updating child: {str(e)}'}), 400
#________________________________________________________________________________________________

@parent_bp.route('/get_children_details/<p_mail>', methods=['GET'])
def get_children_details(p_mail):
    try:
        children = C_INFO.query.filter_by(P_MAIL=p_mail).all()

        children_list = []

        for child in children:
            children_list.append({
                'child_id': child.C_ID,
                'c_name': child.C_NAME,
                'age': child.AGE,
                'dob': str(child.DOB),
                'gender': child.GENDER,
                'blood_type': child.BLOOD_TYPE
            })

        return jsonify({'status': 'success', 'children_details': children_list}), 200
    

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error fetching children details: {str(e)}'}), 500
#_____________________________________________________________________________________________________________________________________
    
@parent_bp.route('/get_parent_details', methods=['POST'])
def get_parent_details():
    try:
        data=request.get_json()
        parent_mail = data.get('parent_mail')
        parent = P_INFO.query.filter_by(MAIL=parent_mail).first()

        if not parent:
            return jsonify({'status': 'error', 'message': 'Parent not found'}), 404

        parent_data = {
            'p_name': parent.P_NAME,
            'address': parent.ADDRESS,
            'contact': parent.CONTACT,
            'city':parent.CITY,
            'children': []  
        }

        children = C_INFO.query.filter_by(P_MAIL=parent_mail).all()
        for child in children:
            parent_data['children'].append({
                'child_id': child.C_ID,
                'c_name': child.C_NAME,
                'age': child.AGE,
                'dob': str(child.DOB),
                'gender': child.GENDER,
                'blood_type': child.BLOOD_TYPE
            })

        return jsonify({'status': 'success', 'parent_details': parent_data}), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error fetching parent details: {str(e)}'}),500

#___________________________________________________________________________________________
@parent_bp.route('/get_child_details/<child_id>', methods=['GET'])
def get_child_details(child_id):
    try:
        print(f"Received child_id: {child_id}")
        child = C_INFO.query.filter_by(C_ID=child_id).first()
        if child:
            child_details = {
                'child_id': child.C_ID,
                'c_name': child.C_NAME,
                'age': child.AGE,
                'dob': str(child.DOB),
                'gender': child.GENDER,
                'blood_type': child.BLOOD_TYPE,
                'p_mail': child.P_MAIL
            }

            return jsonify({'status': 'success', 'child_details': child_details}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Child not found'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error fetching child details: {str(e)}'}), 500

#____________________________________________________________________________________________

@parent_bp.route('/book_appointment', methods=['POST'])
def appointment():
    try:
        data = request.get_json()
        c_id = data.get('c_id')
        h_mail = data.get('h_mail')
        a_date = data.get('date')

        date = datetime.datetime.strptime(a_date, '%Y-%m-%d').date()
        v_name = data.get('v_name')

        h_info = H_INFO.query.get(h_mail)
        if h_info:
            h_name = h_info.H_NAME
        else:
            return jsonify({'status': 'error', 'message': 'Hospital information not found for provided h_mail'}), 404

        appointment = C_INFO.query.filter_by(C_ID=c_id).first()
        if appointment is None:
            return jsonify({'status': 'error', 'message': 'No child found with provided c_id'}), 404

        appointment = APPOINTMENT(
            C_ID=c_id,
            H_NAME=h_name,
            V_NAME=v_name,
            DATE=date
        )
        db.session.add(appointment)
        db.session.commit()
        return jsonify({'status': 'success'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Error deleting child: {str(e)}'}), 400
#_______________________________________________________________________

@parent_bp.route('/update_appointment', methods=['POST'])
def update_appointment():
    try:
        data = request.get_json()

        c_id = data.get('c_id')
        h_mail = data.get('h_mail')
        a_date = data.get('date')
        v_name = data.get('v_name')

        # Validate and parse date
        try:
            date = datetime.datetime.strptime(a_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Invalid date format. Please use YYYY-MM-DD'}), 400

        # Retrieve hospital information
        h_info = H_INFO.query.get(h_mail)
        if not h_info:
            return jsonify({'status': 'error', 'message': 'Hospital information not found for provided h_mail'}), 404
        h_name = h_info.H_NAME

        # Retrieve appointment
        appointment = APPOINTMENT.query.filter_by(C_ID=c_id).first()
        if not appointment:
            return jsonify({'status': 'error', 'message': 'No appointment found with provided c_id'}), 404

        # Update appointment details based on options provided
    
        if 'reschedule' in data:
            appointment.DATE = date
        if 'change_hospital' in data:
            appointment.H_NAME = h_name
        if 'change_vaccination' in data:
            appointment.V_NAME = v_name

        db.session.commit()
        return jsonify({'status': 'success'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Error updating appointment: {str(e)}'}), 400
    
    #_________________________________________________________________________________________________________________________________________________________

@parent_bp.route('/view_appointments', methods=['POST'])
def view_appointments():
    try:
        data=request.get_json()
       
        parent_mail = data.get('p_mail')

        children = C_INFO.query.filter_by(P_MAIL=parent_mail).all()

        appointment_list = []

        for child in children:
            appointments = APPOINTMENT.query.filter_by(C_ID=child.C_ID).all()

            for appointment in appointments:
                appointment_data = {
                    'appointment_id': appointment.AP_ID,
                    'c_name': child.C_NAME,
                    'v_name': appointment.V_NAME,
                    'status': appointment.STATUS,
                    'h_name': appointment.H_NAME,
                    'a_date': appointment.DATE.strftime('%Y-%m-%d') if appointment.DATE else "N/A"
                }
                appointment_list.append(appointment_data)

        return jsonify({'status': 'success', 'appointments': appointment_list}), 200
    

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error fetching parent appointments: {str(e)}'}), 500
    

#_______________________________________________________________________________________________________________________________________________

@parent_bp.route('/view_appointment/<ap_id>', methods=['GET'])
def view_appointment(ap_id):
    try:
        
        appointment = APPOINTMENT.query.get(ap_id)
        if not appointment:
            return jsonify({'status': 'error', 'message': 'Appointment not found'}), 404

        child = C_INFO.query.get(appointment.C_ID)

        appointment_data = {
            'ap_id': appointment.AP_ID,
            'c_name': child.C_NAME if child else "N/A",
            'v_name': appointment.V_NAME,
            'status': appointment.STATUS,
            'h_name': appointment.H_NAME,
            'a_date': appointment.DATE.strftime('%Y-%m-%d') if appointment.DATE else "N/A"
        }

        return jsonify({'status': 'success', 'appointment_details': appointment_data}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error fetching appointment details: {str(e)}'}), 500
    
#_____________________________________________________________________________________________________________________________________
    
@parent_bp.route('/delete_appointment/<ap_id>', methods=['DELETE'])
def delete_appointment(ap_id):
    try:
        appointment = APPOINTMENT.query.get(ap_id)

        if not appointment:
            return jsonify({'status': 'error', 'message': 'Appointment not found'}), 404

        db.session.delete(appointment)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Appointment deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Error deleting appointment: {str(e)}'}), 500