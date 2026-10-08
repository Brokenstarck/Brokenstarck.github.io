from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from config import Config
from .extensions import db, ma, jwt


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    # Registrar blueprints (rutas)
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    # Manejadores de error globales
    @app.errorhandler(HTTPException)
    def handle_http_error(e):
        return jsonify({"error": e.description, "codigo": e.code}), e.code

    @app.errorhandler(Exception)
    def handle_generic_error(e):
        app.logger.exception(e)
        return jsonify({"error": "Error interno del servidor"}), 500

    # Crear tablas (temporal, sin migraciones)
    with app.app_context():
        db.create_all()

    return app