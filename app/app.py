from fastapi import Depends, FastAPI, HTTPException
import uvicorn
from fhir.resources.patient import Patient
from connection import connect_to_mongodb

app = FastAPI()

collection = connect_to_mongodb("SamplePatientService", "patients")

@app.get("/patient/{patient_id}", response_model=Patient)
def get_patient_by_id(patient_id: str):
    patient = collection.find_one({"_id": patient_id})
    if patient:
        return Patient(**patient)
    else:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
