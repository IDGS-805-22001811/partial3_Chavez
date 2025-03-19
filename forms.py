from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,DateField
from wtforms.validators import DataRequired

class AlumnoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido_paterno = StringField('Apellido Paterno', validators=[DataRequired()])
    apellido_materno = StringField('Apellido Materno', validators=[DataRequired()])
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[DataRequired()])
    grupo = SelectField('Grupo', choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], validators=[DataRequired()])
    
class PreguntaForm(FlaskForm):
    pregunta = StringField('Pregunta', validators=[DataRequired()])
    opcion_a = StringField('Opción A', validators=[DataRequired()])
    opcion_b = StringField('Opción B', validators=[DataRequired()])
    opcion_c = StringField('Opción C', validators=[DataRequired()])
    opcion_d = StringField('Opción D', validators=[DataRequired()])
    respuesta_correcta = StringField('Respuesta Correcta (A, B, C o D)', validators=[DataRequired()])
    submit = SubmitField('Agregar Pregunta')
    
class GrupoForm(FlaskForm):
    grupo = SelectField('Seleccionar Grupo', choices=[])
    submit = SubmitField('Ver Calificaciones')
    
class TuFormulario(FlaskForm):
    grupo = SelectField("Grupo", choices=[("A", "Grupo A"), ("B", "Grupo B")])  