from datetime import datetime
from .extensions import db


class Tarea(db.Model):
    __tablename__ = "tareas"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, default="")
    completada = db.Column(db.Boolean, default=False)
    creada_en = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Tarea {self.id}: {self.titulo}>"