from pymongo import MongoClient
from datetime import datetime
from ..config import Config

client = MongoClient(Config.MONGO_URI)
db = client["vuelosDB"]
flights_collection = db["flights"]
flights_collection = db["flights"]

def save_flights(flights):
    """Guarda vuelos en MongoDB (elimina anteriores antes de insertar nuevos)"""
    if not flights:
        return 0


    flights_collection.delete_many({})  # limpiar para mantener solo los actuales

    if flights_collection.insert_many(flights):
        print("Flights inseridos com sucesso")
    flights_collection.insert_many(flights)
    return len(flights)

def get_all_flights():
    """Devuelve los vuelos almacenados"""
    return list(flights_collection.find({}, {"_id": 0}))
