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
