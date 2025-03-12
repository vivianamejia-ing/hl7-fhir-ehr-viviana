from connection import connect_to_mongodb
from bson import ObjectId
from fhir.resources.Patient import Patient
import json

collection = connect_to_mongodb("SamplePatientService", "patients")

def GetPatientById(patient_id: str):
    try:
        patient = collection.find_one({"_id": ObjectId(patient_id)})
        patient["_id"] = str(patient["_id"])
        if patient:
            return "success", patient
        return "notFound", None
    except:
        return "error", None

def WritePatient(patient_dict: dict):
    try:
        pat = Patient.model_validate(patient_dict)
    except Exception as e:
        return f"errorValidating: {str(e)}",None
    validated_patient_json = pat.model_dump()
    result = collection.insert_one(validated_patient_json)
    if result:
        inserted_id = str(result.inserted_id)
        return "success",inserted_id
    else:
        return "errorInserting", None