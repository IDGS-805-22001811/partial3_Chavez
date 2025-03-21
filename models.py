from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class Alumno(db.Model):
    __tablename__ = 'alumnos'  
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido_paterno = db.Column(db.String(50), nullable=False)
    apellido_materno = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.String(10), nullable=False)
    grupo = db.Column(db.String(10), nullable=False)


class Pregunta(db.Model):
    __tablename__ = 'preguntas'  
    id = db.Column(db.Integer, primary_key=True)
    pregunta = db.Column(db.String(255), nullable=False)
    opcion_a = db.Column(db.String(50), nullable=False)
    opcion_b = db.Column(db.String(50), nullable=False)
    opcion_c = db.Column(db.String(50), nullable=False)
    opcion_d = db.Column(db.String(50), nullable=False)
    respuesta_correcta = db.Column(db.String(1), nullable=False)


class Respuesta(db.Model):
    __tablename__ = 'respuesta'  
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'))  
    pregunta_id = db.Column(db.Integer, db.ForeignKey('preguntas.id'))  
    respuesta_alumno = db.Column(db.String(1))
    
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Base de datos simulada de usuarios (puedes cambiar esto por SQLAlchemy)
users = {
    "admin": User(id=1, username="admin", password="1234"),
    "user": User(id=2, username="user", password="password"),
}
