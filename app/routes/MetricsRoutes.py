from flask import Blueprint, jsonify
from ..services.open_sky_client import get_flights_over_cdmx
from ..services.db_manager import flights_collection

#Creamos el blueprint
metrics_bp = Blueprint('metrics', __name__, url_prefix='/metrics')

@metrics_bp.route('/flight_count')
def get_flight_count():
    count = flights_collection.count_documents({})
    return jsonify({"count": count})

@metrics_bp.route('/last_update')
def last_update():
    last = flights_collection.find_one(sort=[("_id", -1)])
    return jsonify({"timestamp": last["timestamp"]})
@metrics_bp.route("/stats")
def stats_overview():
    total = flights_collection.count_documents({})
    en_vuelo = flights_collection.count_documents({"on_ground": False})
    en_tierra = total - en_vuelo

    # Promedio velocidad
    promedio_vel_cursor = list(
        flights_collection.aggregate([{"$group": {"_id": None, "avgVel": {"$avg": "$velocity"}}}])
    )
    promedio_vel = promedio_vel_cursor[0]["avgVel"] if promedio_vel_cursor else 0

    # Promedio altitud
    promedio_alt_cursor = list(
        flights_collection.aggregate([{"$group": {"_id": None, "avgAlt": {"$avg": "$baro_altitude"}}}])
    )
    promedio_alt = promedio_alt_cursor[0]["avgAlt"] if promedio_alt_cursor else 0

    return jsonify({
        "total_vuelos": total,
        "en_vuelo": en_vuelo,
        "en_tierra": en_tierra,
        "promedio_velocidad": promedio_vel,
        "promedio_altitud": promedio_alt
    })