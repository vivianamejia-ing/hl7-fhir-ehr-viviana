from fastapi import FastAPI, HTTPException, Request
import uvicorn
from app.controlador.PatientCrud import GetPatientById,WritePatient
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solo este dominio
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.get("/patient/{patient_id}", response_model=dict)
async def get_patient_by_id(patient_id: str):
    status,patient = GetPatientById(patient_id)
    if status=='success':
        return patient  # Return patient
    elif status=='notFound':
        raise HTTPException(status_code=404, detail="Patient not found")
    else:
        raise HTTPException(status_code=500, detail=f"Internal error. {status}")

@app.get("/patient", response_model=dict)
async def get_patient_by_id_identifier(system: str, value: str):
    status,patient = GetPatientByIdIdentifier(patient_id)
    if status=='success':
        return patient  # Return patient
    elif status=='notFound':
        raise HTTPException(status_code=404, detail="Patient not found")
    else:
        raise HTTPException(status_code=500, detail=f"Internal error. {status}")

@app.post("/patient", response_model=dict)
async def add_patient(request: Request):
    new_patient_dict = dict(await request.json())
    status,patient_id = WritePatient(new_patient_dict)
    if status=='success':
        return {"_id":patient_id}  # Return patient id
    else:
        raise HTTPException(status_code=500, detail=f"Validating error: {status}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import random
import time
import uuid

app = FastAPI()

# Modelo Pydantic para solicitud de nueva imagen
class NuevaImagen(BaseModel):
    paciente: str
    kvp: int = 120
    mas: float = 2.5

# Modelo Pydantic para respuesta de imagen
class ImagenRespuesta(BaseModel):
    id_imagen: str
    paciente: str
    calidad: str
    informe: Optional[str] = None
    estado: str

# Base de datos simulada
db_imagenes = {}

@app.get("/imagenes/{id_imagen}", response_model=ImagenRespuesta)
def obtener_imagen(id_imagen: str):
    """Obtener detalles de una imagen por ID (GET)"""
    if id_imagen not in db_imagenes:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return db_imagenes[id_imagen]

@app.post("/imagenes/", response_model=ImagenRespuesta)
def crear_imagen(imagen: NuevaImagen):
    """Crear una nueva imagen radiológica (POST)"""
    # Paso 1: Generar un ID único
    id_imagen = str(uuid.uuid4())
    
    # Paso 2: Simular adquisición (calidad aleatoria)
    calidad = random.choice(["Buena", "Aceptable", "Pobre"])
    
    # Paso 3: Procesamiento (simulado)
    time.sleep(1)
    
    # Paso 4: Generar informe si la imagen es válida
    informe = None
    if calidad in ["Buena", "Aceptable"]:
        informe = f"Informe radiológico para {imagen.paciente}. Calidad: {calidad}"
    
    # Guardar en "base de datos" simulada
    db_imagenes[id_imagen] = {
        "id_imagen": id_imagen,
        "paciente": imagen.paciente,
        "calidad": calidad,
        "informe": informe,
        "estado": "Completado" if informe else "Requiere repetición"
    }
    
    return db_imagenes[id_imagen]

@app.get("/imagenes/")
def listar_imagenes():
    """Listar todas las imágenes almacenadas (GET)"""
    return db_imagenes