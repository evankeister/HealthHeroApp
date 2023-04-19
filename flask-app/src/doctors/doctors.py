from flask import Blueprint, request, jsonify, make_response
import json
from src import db


doctors = Blueprint('doctors', __name__)

# Get a list of patient information for one doctor
@doctors.route('/patient_names', methods=['GET'])
def get_patient_name_list():  
   # get a cursor object from the database
   cursor = db.get_db().cursor()
   
   # collect user-inputted data from form
   req_data = request.get_json() 
   DoctorID = req_data['DoctorID_patient_names']

   # use cursor to query the database for a list of patient info using DoctorID
   query = 'SELECT Patient.fName as PatientFirstName, Patient.lName as PatientLastName, SSN, DOB, Emails.Email '
   query += 'FROM Doctor JOIN Doctor_treats_Patient using(DoctorID) '
   query += 'JOIN Patient using(SSN) '
   query += 'Join Emails using(SSN)'
   query += 'WHERE Doctor.DoctorID = ' + str(DoctorID)
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
 
# Get a list of appointments for one doctor
@doctors.route('/view_appointments', methods=['GET'])
def view_appointments():   
   # get a cursor object from the database
   cursor = db.get_db().cursor()

   # collect user-inputted data from form
   req_data = request.get_json()
   DoctorID = req_data['DoctorID_view_appointments']

   # use cursor to query the database a list of appointments using DoctorID
   query = 'SELECT AppointmentDate, SSN, Patient.fName as PatientFirstName, Patient.lName as PatientLastName, DOB '
   query += 'FROM Doctor JOIN Doctor_treats_Patient using(DoctorID) '
   query += 'JOIN Patient using(SSN) '
   query += 'WHERE Doctor.DoctorID = ' + str(DoctorID)
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

# Get a list of medical conditions for one patient
@doctors.route('/patient_medical_conditions', methods=['GET'])
def get_patient_medical_condtions():   
   # get a cursor object from the database
   cursor = db.get_db().cursor()
   
   # collect user-inputted data from form
   req_data = request.get_json()
   DoctorID = req_data['DoctorID_Med_Hist']
   PatientFirstName = req_data['Patient_FirstName']
   PatientLastName = req_data['Patient_LastName']
   PatientSSN = req_data['Patient_SSN']
   
   # use cursor to query the database for a list of medical conditions using patient info
   query = 'SELECT ConditionID, ConditionName, DateDiscovered, Prevalence, TreatmentOptions, Transmissible, Causes, Severity '
   query += 'FROM Patient JOIN Patient_diagnosed_MedicalCondition using(SSN) '
   query += 'JOIN MedicalCondition USING(ConditionID) '
   query += 'WHERE Patient.SSN = ' + str(PatientSSN)
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
 
# View info on all medical conditions from the entire database
@doctors.route('/view_medical_conditions_in_database', methods=['GET'])
def view_medical_conditions_in_database():
   # get a cursor object from the database
   cursor = db.get_db().cursor()

   # use cursor to query the database for the entire MedicalCondition table
   query = 'Select * From MedicalCondition'
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
 
# Daignose a patient with a new medical condition
@doctors.route('/diagnose', methods=['POST'])
def diagnose():
   # get a cursor object from the database
   cursor = db.get_db().cursor()

   # collect user-inputted data from form
   req_data = request.get_json()
   ConditionID = req_data['ConditionID']
   SSN = req_data['SSN_diagnose']
   
   # generate insert statement to add a medical condition to one patient
   insert_stmt = 'INSERT INTO Patient_diagnosed_MedicalCondition (ConditionID, SSN) '
   insert_stmt += 'VALUES (' + str(ConditionID) + ', ' + str(SSN) + ')'
   cursor.execute(insert_stmt)
   
   # commit changes
   db.get_db().commit()
   
   output = 'Successfully diagnose patinet: ' + str(SSN) + ', with condition: ' + str(ConditionID)
   return output
 
# Cancel an appoitment with a patient
@doctors.route('/cancel_appointment', methods=['DELETE'])
def cancel_appointment():
   # get a cursor object from the database
   cursor = db.get_db().cursor()

   # collect user-inputted data from form
   req_data = request.get_json()
   SSN_1 = req_data['SSN_delete']
   doctor_ID = req_data['DoctorID_delete']
   appointment_data = req_data['AppointmentDate_delete']

   # generate delete statement to remove appointment uusing Patient SSN, DoctorID, and AppointmentDate
   delete_stmt = 'DELETE From Doctor_treats_Patient '
   delete_stmt += 'WHERE SSN = ' + str(SSN_1) + ' AND DoctorID = ' + str(doctor_ID) + " AND AppointmentDate = '" + appointment_data + "'"
   cursor.execute(delete_stmt)

   # commit changes
   db.get_db().commit()

   return 'Successfully canceled the appointment'
 
 
# Update specialty of interest for one doctor
@doctors.route('/update_specialty', methods=['PUT'])
def update_specialty():
   # get a cursor object from the database
   cursor = db.get_db().cursor()
   
   # collect user-inputted data from form
   req_data = request.get_json()
   DoctorID = req_data['DoctorID_update_specialty']
   Specialty = req_data['Specialty_update']

   # generate update statement to change doctor specialty
   update_stmt = 'UPDATE Doctor '
   update_stmt += "SET Specialty = '" + Specialty + "' "
   update_stmt += 'WHERE DoctorID = ' + str(DoctorID)
   cursor.execute(update_stmt)

   # commit changes
   db.get_db().commit()

   return 'Successfully changed specialty to: ' + str(Specialty) + ', Doctor: ' + str(DoctorID)
 
# View the medications that are being prescribed to one of a doctor's patients
@doctors.route('/view_medication_prescribed_to_patient', methods=['GET'])
def view_medication_prescribed_to_patient():
   # get a cursor object from the database
   cursor = db.get_db().cursor()
   
   # collect user-inputted data from form
   req_data = request.get_json()
   DoctorID = req_data['DoctorID_medications']
   SSN = req_data['SSN_medications']

   # query the database for medication information using patient SSN and DoctorID
   query = 'Select MedicationCommonName, Dosage, BrandName, GenericName, Med_Description FROM Patient join Prescription using(SSN) '
   query += 'join Medication using(MedID)'
   #query = 'Select MedicationCommonName, BrandName, Dosage, '
   #query += 'GenericName, Med_Description, Patient.SSN '
   #query += 'FROM Patient join Prescription using(SSN) '
   #query += 'join Medication using(MedID) '
   #query += 'WHERE Patient.SSN = ' + str(SSN)
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
 
# Get a list of pharmacies that have medications for a patient
@doctors.route('/see_what_pharmacies_have_medications_for_patient', methods=['GET'])
def see_what_pharmacies_have_medications_for_patient():
   # get a cursor object from the database
   cursor = db.get_db().cursor()
   
   # collect user-inputted data from form
   req_data = request.get_json()
   DoctorID = req_data['DoctorID_meds_pharms']
   SSN = req_data['SSN_meds_pharms']

   # query the database for a list of pharmacies using patient SSN and DoctorID
   query = 'Select CompanyName, City, State, Zip, P.Phone '
   query += 'FROM Doctor join Doctor_treats_Patient using(DoctorID) '
   query += 'join Patient using(SSN) '
   query += 'join Prescription using(DoctorID) '
   query += 'join Medication using(MedID) '
   query += 'join Pharmacy_contains_Medication using(MedID) '
   query += 'join Pharmacy P on Pharmacy_contains_Medication.PharmID = P.PharmID '
   query += 'WHERE Patient.SSN = ' + str(SSN) + ' AND Doctor.DoctorID = ' + str(DoctorID)
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

# Get a list of reviews for a doctor
@doctors.route('/get_reviews', methods=['GET'])
def get_reviews():  
   # get a cursor object from the database
   cursor = db.get_db().cursor()

   # collect user-inputted data from form
   req_data = request.get_json()
   DoctorID = req_data['DoctorID_get_reviews']

   # use cursor to query the database for doctor reviews using DoctorID
   query = 'SELECT * FROM DoctorReviews '
   query += 'WHERE DoctorID = ' + str(DoctorID)
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

