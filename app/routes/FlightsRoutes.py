from flask import Blueprint, jsonify,request

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


@flights_bp.route("/status", methods=["GET"])
def flight_status():
    callsign = request.args.get("callsign")
    if not callsign:
        return jsonify({"error": "No callsign provided"}), 400

    # Buscar vuelo en la base de datos
    vuelo = mongo.db.flights.find_one({"callsign": callsign.strip()})
    if not vuelo:
        return jsonify({"status": "not_found"}), 404

    lat = vuelo.get("latitude", 0)
    lon = vuelo.get("longitude", 0)

    # Coordenadas aproximadas de CDMX
    if 19.2 <= lat <= 19.6 and -99.3 <= lon <= -98.9:
        status = "in_cdmx"
    else:
        status = "in_air"

    return jsonify({
        "callsign": callsign,
        "status": status,
        "latitude": lat,
        "longitude": lon,
        "velocity": vuelo.get("velocity", 0),
        "altitude": vuelo.get("baro_altitude", 0)
    })

@flights_bp.route("/discovery", methods=["GET"])
def flights_discovery():
    # Obtener vuelos registrados en MongoDB
    tracked = list(mongo.db.flights.find())
    return jsonify({
        "data": [{"{#CALLSIGN}": f.get("callsign").strip()} for f in tracked]
    })

