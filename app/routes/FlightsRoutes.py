from flask import Blueprint, request, jsonify
from .. import mongo

#Creamos el blueprint
flights_bp = Blueprint('flights', __name__, url_prefix='/flights')

@flights_bp.route('/')
def hello():
    return '¡Hola, mundo!'

@flights_bp.route('/test')
def test_connection():
    data = request.get_json()

    # Insertar en la colección 'tests'
    result = mongo.vuelosDB.hack.insert_one({
        "name": data.get("name", "sin_nombre"),
        "message": data.get("message", "sin_mensaje")
    })

    return jsonify({
        "status": "success",
        "inserted_id": str(result.inserted_id)
    }), 201