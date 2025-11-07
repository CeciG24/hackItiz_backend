from flask import Blueprint, jsonify
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
    