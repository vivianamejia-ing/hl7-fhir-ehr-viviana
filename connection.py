from pymongo import MongoClient
from pymongo.server_api import ServerApi


def connect_to_mongodb(db_name, collection_name):
    uri = "mongodb+srv://karolamejia08:SlKXrpUHjTxV9QWC@patient.gz8al.mongodb.net/?retryWrites=true&w=majority&appName=Patient"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[db_name]
    collection = db[collection_name]
    return collection
    db_name = "patient"
    collection_name = "pacientes"
    collection = connect_to_mongodb(db_name, collection_name)
    paciente_id = collection.insert_one(paciente).inserted_id

    # Devolver una respuesta
    return jsonify({"mensaje": "Paciente guardado correctamente", "id": str(paciente_id)})
