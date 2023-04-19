from flask import Blueprint, request, jsonify, make_response
import json
from src import db
import random
import datetime

patients = Blueprint('patients', __name__)

# Get all of the doctor names in the database, and if they are MD or DO
@patients.route('/doctornames', methods=['GET'])
def get_doctor_names():
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    
    # use cursor to query the database for a list of products
    cursor.execute('Select fName as FirstName, lName as LastName, MDorDO FROM Doctor')

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

# Get all of the doctor names in the database, and if they are MD or DO
@patients.route('/view_medical_conditions', methods=['GET'])
def view_medical_conditions():
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    
    # collect user-inputted data from form
    req_data = request.get_json()
    SSN = req_data['SSN_view_medical_conditinos']

    # query the database for medical conditions using patient SSN
    query =  'Select ConditionName, DateDiscovered, TreatmentOptions, Transmissible, Causes, Severity '
    query += 'FROM Patient join Patient_diagnosed_MedicalCondition PdMC using(SSN) '
    query += 'join MedicalCondition using(ConditionID) '
    query += 'WHERE Patient.SSN = ' + str(SSN)
    cursor.execute(query)

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

# Get all of the doctor names in the database, and if they are MD or DO
@patients.route('/view_your_appointments', methods=['GET'])
def view_your_appointments():
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    
    # collect user-inputted data from form
    req_data = request.get_json()
    patient_SSN = req_data['SSN_appointment_view']

    # query the database for appointments using patient SSN
    query = 'Select AppointmentDate, DoctorID, Doctor.fName as DoctorFirstName, Doctor.lName as DoctorLastName, Cost '
    query += 'FROM Patient join Doctor_treats_Patient using(SSN) '
    query += 'join Doctor using(DoctorID) '
    query += 'WHERE SSN = ' + str(patient_SSN)
    cursor.execute(query)

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
       json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

# Schedule an appointment with a doctor
@patients.route('/make_an_appointment', methods=['POST'])
def make_an_appointment():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # collect user-inputted data from form
    req_data = request.get_json()
    appointmentDate = req_data['AppointmentDate']
    doctor_id = req_data['DoctorID_make_appointment']
    SSN = req_data['SSN_make_appointment']
    Cost = round(random.uniform(1000.00, 10000.00), 2)
    
    # generate insert statement for a new appointment with patient SSN and DoctorID
    insert_stmt = 'INSERT INTO Doctor_treats_Patient (DoctorID,SSN,AppointmentDate,Cost) '
    insert_stmt += 'VALUES (' + str(doctor_id) + ", " + str(SSN) + ', "' + appointmentDate + '", ' + str(Cost) + ")"
    cursor.execute(insert_stmt)

    # commit changes
    db.get_db().commit()
    
    output = 'Successfully scheduled an appoitment with ' + str(doctor_id) + ' on + ' + appointmentDate + "."
    return output

# Get list of prescriptions for one patient
@patients.route('/get_prescription_list', methods=['GET'])
def get_prescription_list():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # collect user-inputted data from form
    req_data = request.get_json()
    SSN_1 = req_data['SSN_get_prescription']

    # query the database for prescriptions using patient SSN
    query = 'Select MedicationCommonName, Dosage '
    query += 'FROM Patient join Prescription using (SSN) '
    query += 'WHERE SSN = ' + str(SSN_1)
    cursor.execute(query)

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
       json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

# Delete appointment with a doctor
@patients.route('/delete_appointment', methods=['DELETE'])
def delete_appoitment():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # collect user-inputted data from form
    req_data = request.get_json()
    SSN_1 = req_data['SSN_delete']
    doctor_ID = req_data['DoctorID_delete']
    appointment_data = req_data['AppointmentDate_delete']

    # generate delete statement to remove appointment with patient SSN, DoctorID, and AppointmentDate
    delete_stmt = 'DELETE From Doctor_treats_Patient '
    delete_stmt += 'WHERE SSN = ' + str(SSN_1) + ' AND DoctorID = ' + str(doctor_ID) + " AND AppointmentDate = '" + appointment_data + "'"
    cursor.execute(delete_stmt)

    # commit changes
    db.get_db().commit()

    return 'Successfully deleted the appoitment'

# Update the email for one patient
@patients.route('/update_email', methods=['PUT'])
def update_email():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # collect user-inputted data from form
    req_data = request.get_json()
    SSN = req_data['SSN_email']
    new_email = req_data['new_email']
    old_emal = req_data['old_email']

    # generate update statement to change email with patient SSN
    update_stmt = 'UPDATE Emails '
    update_stmt += "SET Email = '" + new_email + "' "
    update_stmt += 'WHERE SSN = ' + str(SSN) + " AND Email = '" + old_emal + "'"
    cursor.execute(update_stmt)

    # commit changes
    db.get_db().commit()

    return 'Successfully updated email'

# See the insurance info for one patient
@patients.route('/get_insurance_info', methods=['GET'])
def get_insurance_info():
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    
    # collect user-inputted data from form
    req_data = request.get_json()
    SSN = req_data['SSN_insurance']

    # query the database to get insurance info from patient SSN
    query = 'Select CompanyName, Coverage, Expiration, PlanType '
    query += 'FROM Patient join Insurance using (CompanyID) '
    query += 'WHERE Patient.SSN = ' + str(SSN)
    cursor.execute(query)

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
       json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

# Create a doctor review
@patients.route('/add_doctor_review', methods=['POST'])
def add_doctor_review():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # collect user-inputted data from form
    req_data = request.get_json()
    rating = req_data['Doctor Rating']
    rev_description = req_data['Review Description']
    doctor_id = req_data['DoctorID']
    
    # generate insert statement to add a doctor review 
    insert_stmt = 'INSERT INTO DoctorReviews (Rating, Rev_Description, DoctorID)'
    insert_stmt += 'VALUES (' + str(rating) + ', "' + rev_description + '", ' + str(doctor_id) + ")"
    cursor.execute(insert_stmt)

    # commit changes
    db.get_db().commit()
    
    output = 'Successfully submitted review for ' + str(doctor_id) + '  "' +  '.'

# Get info on practices which accept a specific insurance
@patients.route('/get_practice_info', methods=['GET'])
def get_practice_info():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # collect user-inputted data from form
    req_data = request.get_json()
    company_id = req_data['Insurance Company ID']

    # uquery the database to retrieve practices using CompanyID
    query = 'SELECT * FROM Practice JOIN Practice_accepts_Insurance USING (PracticeNumber)'
    query += 'WHERE CompanyID = ' + str(company_id)
    cursor.execute(query)

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
       json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)