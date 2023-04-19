from flask import Blueprint, request, jsonify, make_response
import json
from src import db


pharmacist = Blueprint('pharmacist', __name__)

# Get a list of all the medications that are supplied by the pharmacy that a pharmacist works at
@pharmacist.route('/pharmacy_meds', methods=['GET'])
def get_pharmacy_medications():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # collect user-inputted data from form
    req_data = request.get_json()
    EmployeeID = req_data['EmployeeID_pharmacy_meds']

    # query the database for a list of medications at one pharmacy using EmployeeID
    query = 'Select MedID, PharmID, QtyInStock, GenericName as MedicationName, BrandName as Manufacturer, Med_Description as Description, QtyInStock, UnitCost '
    query += 'FROM Pharmacist join Pharmacy using(PharmID) join Pharmacy_contains_Medication using(PharmID) '
    query += 'join Medication using(MedID) '
    query += 'WHERE EmployeeID = ' + str(EmployeeID)
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

# Update medicine quantity in stock
@pharmacist.route('/update_medication_inventory', methods=['PUT'])
def update_medication_inventory():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # collect user-inputted data from form
    req_data = request.get_json()
    MedID = req_data['MedID_update']
    PharmID = req_data['PharmID_update']
    new_qty = req_data['new_qty_update']

    # generate update statement to change inventory levels for one medicine
    update_stmt = 'UPDATE Pharmacy_contains_Medication '
    update_stmt += "SET QtyInStock = " + str(new_qty) + " "
    update_stmt += 'WHERE MedID = ' + str(MedID) + " AND PharmID = " + str(PharmID) + ""
    cursor.execute(update_stmt)

    # commit changes
    db.get_db().commit()

    return 'Successfully updated medicine stock'

# Delete medication
@pharmacist.route('/delete_medication', methods=['DELETE'])
def delete_medication():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # collect user-inputted data from form
    req_data = request.get_json()
    MedID = req_data['MedID_delete']

    # generate delete statement to remove medication from a Medication table
    delete_stmt = 'Delete From Medication '
    delete_stmt += 'WHERE MedID = ' + str(MedID)
    cursor.execute(delete_stmt)

    # commit changes
    db.get_db().commit()

    return 'Successfully deleted the medication'

# Delete prescription
@pharmacist.route('/delete_prescription', methods=['DELETE'])
def delete_prescription():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # collect user-inputted data from form
    req_data = request.get_json()
    Presc_ID = req_data['Presc_ID']

    # generate delete statement to remove a prescription order
    delete_stmt = 'DELETE From Prescription '
    delete_stmt += 'WHERE PrescID = ' + str(Presc_ID)
    cursor.execute(delete_stmt)

    # commit changes
    db.get_db().commit()

    return 'Successfully deleted the prescription'

# Add medication
@pharmacist.route('/add_medication', methods=['POST'])
def add_medication():
    # get a cursor object from the database
    cursor = db.get_db().cursor()
 
    # collect user-inputted data from form
    req_data = request.get_json()
    Med_ID = req_data['MedID_add']
    brandName = req_data['BrandName_add']
    genericName = req_data['genericName_add']
    medDescription = req_data['med_descriptionAdd']
    
    # generate insert statement to add a medication to the Medication table 
    insert_stmt = 'INSERT INTO Medication (MedID,BrandName,GenericName,Med_Description) '
    insert_stmt += 'VALUES (' + str(Med_ID) + ", '" + brandName + "', '" + genericName + "', '" + medDescription + "')"
    cursor.execute(insert_stmt)

    # commit changes
    db.get_db().commit()
    
    output = "Successfully added medication."
    return output

# Get perscriptions for a certain patient
@pharmacist.route('/get_prescription', methods=['GET'])
def get_pharmacy_medications_2():
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    
    # collect user-inputted data from form
    req_data = request.get_json()
    SSN = req_data['SSN_get_prescription']

    # query the database for a list of prescriptions for a certain patient
    query = 'Select * FROM Patient join Prescription using (SSN) '
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

# Get list of chemical compounds for medications in a patient's prescription
@pharmacist.route('/get_chemicalcompounds', methods=['GET'])
def get_chemicalcompounds():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # collect user-inputted data from form
    req_data = request.get_json()
    SSN = req_data['SSN_getchemicalcompounds']

    # query the database for a list of products
    query = 'SELECT ScientificName, CommonName, MolecularWeight, BoilingPoint, MeltingPoint, ChemID '
    query += 'FROM Patient JOIN Prescription USING (SSN) '
    query += 'JOIN Medication USING(MedID) '
    query += 'JOIN Medication_contains_ChemicalCompounds USING(MedID) '
    query += 'JOIN ChemicalCompounds USING(ChemID) '
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

# add new education for a pharmacist
@pharmacist.route('/add_new_education', methods=['POST'])
def add_new_education():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # collect user-inputted data from form
    req_data = request.get_json()
    EmployeeID_add_education = req_data['EmployeeID_education_add']
    institution_id_education_add = req_data['InstitutionID_education_add']
    start_year = req_data['start_year']
    end_year = req_data['end_year']
    degree = req_data['degree']
    
    # generate insert statement to add new education information to a pharmacy employee
    insert_stmt = 'INSERT INTO Pharmacist_attended_EducationalInstitute (EmployeeID,InstitutionID,startYear,endYear,Degree) '
    insert_stmt += 'VALUES (' + str(EmployeeID_add_education) + ', ' + str(institution_id_education_add)
    insert_stmt += ', ' + str(start_year) + ', ' + str(end_year) + ", '" + degree + "')"
    cursor.execute(insert_stmt)

    # commit changes
    db.get_db().commit()
    
    output = "Successfully added education."
    return output

