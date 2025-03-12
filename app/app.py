from fastapi import Depends, FastAPI, HTTPException
import uvicorn
from fhir.resources.patient import Patient
from connection import connect_to_mongodb
from bson import ObjectId
import json

app = FastAPI()

collection = connect_to_mongodb("SamplePatientService", "patients")

@app.get("/patient/{patient_id}", response_model=dict)
def get_patient_by_id(patient_id: str):
    patient = collection.find_one({"_id": ObjectId(patient_id)})
    patient["_id"] = str(patient["_id"])
    print("patient:::", patient)
    if patient:
        patient_validate = patient.copy()
        del patient_validate["_id"]
        pat = Patient.model_validate_json(json.dumps(patient_validate))
        if pat.get_resource_type() == "Patient":
            return patient  # Return patient
        else:
            raise HTTPException(status_code=401, detail="Patient not well formatted")
    else:
        raise HTTPException(status_code=404, detail="Patient not found")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
