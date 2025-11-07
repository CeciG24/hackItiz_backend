from flask import Blueprint, jsonify
from datetime import datetime

from app.services.db_manager import flights_collection

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "oki"}), 200

@health_bp.route('/status', methods=['GET'])
def get_system_status():
    return jsonify({
        "data": {
            "api_status": "online",
            "database_status": "online",
            "zabbix_status": "online",
            "total_records": flights_collection.count_documents({}),
            "last_update": datetime.now().isoformat()
        }
    })

