from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from .extensions import db
from .models import Tarea
from .schemas import tarea_schema, tareas_schema

api_bp = Blueprint("api", __name__)


# -------- Ping (ya lo tenías, lo dejamos) --------
@api_bp.get("/ping")
def ping():
    return jsonify({"mensaje": "pong"}), 200


# -------- GET /api/v1/tareas --------
@api_bp.get("/tareas")
def listar_tareas():
    tareas = Tarea.query.order_by(Tarea.id).all()
    return jsonify(tareas_schema.dump(tareas)), 200


# -------- GET /api/v1/tareas/<id> --------
@api_bp.get("/tareas/<int:id>")
def obtener_tarea(id):
    tarea = db.session.get(Tarea, id)
    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404
    return jsonify(tarea_schema.dump(tarea)), 200


# -------- POST /api/v1/tareas --------
@api_bp.post("/tareas")
def crear_tarea():
    try:
        data = tarea_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"errores": err.messages}), 400

    db.session.add(data)
    db.session.commit()
    return jsonify(tarea_schema.dump(data)), 201


# -------- PUT /api/v1/tareas/<id> --------
@api_bp.put("/tareas/<int:id>")
def actualizar_tarea(id):
    tarea = db.session.get(Tarea, id)
    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404

    try:
        data = tarea_schema.load(request.get_json() or {}, partial=True)
    except ValidationError as err:
        return jsonify({"errores": err.messages}), 400

    # Actualización campo a campo
    for campo, valor in data.items():
        setattr(tarea, campo, valor)

    db.session.commit()
    return jsonify(tarea_schema.dump(tarea)), 200


# -------- DELETE /api/v1/tareas/<id> --------
@api_bp.delete("/tareas/<int:id>")
def eliminar_tarea(id):
    tarea = db.session.get(Tarea, id)
    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404

    db.session.delete(tarea)
    db.session.commit()
    return "", 204