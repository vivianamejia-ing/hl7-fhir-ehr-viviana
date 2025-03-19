from pymongo import MongoClient
from pymongo.server_api import ServerApi


def connect_to_mongodb(db_name, collection_name):
    uri = "mongodb+srv://karolamejia08:SlKXrpUHjTxV9QWC@patient.gz8al.mongodb.net/?retryWrites=true&w=majority&appName=Patient"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[db_name]
    collection = db[collection_name]
    return collection
@app.route('/guardar_paciente', methods=['POST'])
def guardar_paciente():
    #Obtener los datos del formulario
    nombre = request.form.get('nombre')
    edad = int(request.form.get('edad'))
    genero = request.form.get('genero')
    diagnostico = request.form.get('diagnostico')
    fecha_ingreso = request.form.get('fecha_ingreso')
