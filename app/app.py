from fastapi import Depends, FastAPI, HTTPException, Request
import uvicorn
from app.controlador.PatientCrud import GetPatientById,WritePatient

app = FastAPI()

@app.get("/patient/{patient_id}", response_model=dict)
def get_patient_by_id(patient_id: str):
    status,patient = GetPatientById(patient_id)
    if status=='success':
        return patient  # Return patient
    elif status=='notFound':
        raise HTTPException(status_code=404, detail="Patient not found")
    else:
        raise HTTPException(status_code=500, detail="Internal error")


@app.post("/patient", response_model=dict)
def add_patient(request: Request):
    new_patient_dict = request
    print("new_patient_dict::",new_patient_dict)
    print(type("new_patient_dict"))
    status,patient_id = WritePatient(new_patient_dict)
    if status=='success':
        return patient_id  # Return patient
    else:
        raise HTTPException(status_code=500, detail=f"Validating error: {status}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
