from flask import Blueprint, jsonify

from .. import mongo
from ..services.open_sky_client import get_flights_over_cdmx
from ..services.db_manager import save_flights, get_all_flights

#Creamos el blueprint
flights_bp = Blueprint('flights', __name__, url_prefix='/flights')

@flights_bp.route("/update_flights", methods=["GET"])
def update_flights():
    try:
        flights = get_flights_over_cdmx()
        count = save_flights(flights)
        return jsonify({"message": f"{count} vuelos guardados correctamente."})
    except Exception as e:
        return jsonify({"error": str(e)})

@flights_bp.route("/", methods=["GET"])
def get_flights():
    try:
        flights = get_all_flights()
        return jsonify(flights)
    except Exception as e:
        return jsonify({"error": str(e)})


@flights_bp.route("/info", methods=["GET"])
def flights_info():
    # Obtener los últimos 5 vuelos ordenados por timestamp descendente
    last_flights = list(mongo.db.flights.find().sort("timestamp", -1).limit(5))

    # Crear resumen
    resumen = []
    for vuelo in last_flights:
        resumen.append({
            "icao24": vuelo.get("icao24", ""),
            "callsign": vuelo.get("callsign", "").strip(),
            "origin_country": vuelo.get("origin_country", ""),
            "altitude": vuelo.get("baro_altitude", 0),
            "velocity": vuelo.get("velocity", 0),
            "lat": vuelo.get("latitude", 0),
            "lon": vuelo.get("longitude", 0)
        })
    print(resumen)
    return jsonify({"vuelos_recientes": resumen}), 200