from marshmallow import fields, validate
from .extensions import ma
from .models import Tarea


class TareaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tarea
        load_instance = True
        include_fk = True

    # Validaciones explícitas
    titulo = fields.String(
        required=True,
        validate=validate.Length(min=1, max=120),
    )
    descripcion = fields.String(load_default="")
    completada = fields.Boolean(load_default=False)


tarea_schema = TareaSchema()
tareas_schema = TareaSchema(many=True)