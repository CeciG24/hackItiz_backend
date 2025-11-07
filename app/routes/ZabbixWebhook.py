# app/routes/ZabbixWebhook.py

from pymongo import MongoClient
from flask import Blueprint, request, jsonify
from ..config import Config
from datetime import datetime

# Conexión a Mongo
client = MongoClient(Config.MONGO_URI)
db = client["vuelosDB"]
alerts_collection = db["alerts"]

# Blueprint
zabbix_bp = Blueprint("zabbix", __name__, url_prefix="/zabbix")

# Endpoint para recibir alertas desde Zabbix
@zabbix_bp.route("/webhook", methods=["POST"])
def zabbix_webhook():
    try:
        data = request.get_json()  # ahora sí recibimos JSON
        if not data:
            return jsonify({"error": "No data received"}), 400

        # Agregar timestamp
        data["received_at"] = datetime.utcnow()

        # Guardar en MongoDB
        alerts_collection.insert_one(data)

        return jsonify({"status": "success", "data_received": data}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint para consultar alertas (para frontend)
@zabbix_bp.route("/alerts", methods=["GET"])
def get_alerts():
    try:
        alerts = list(alerts_collection.find({}, {"_id": 0}))
        return jsonify(alerts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
