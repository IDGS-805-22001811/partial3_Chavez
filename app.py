from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db,Alumno,Pregunta,Respuesta
import forms,datetime
from forms import AlumnoForm, PreguntaForm,GrupoForm,TuFormulario
from flask import flash

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

@app.route("/index")
def index():
    
    return render_template("index.html")


@app.route('/alumno', methods=['GET', 'POST'])
def alumno():
    form = AlumnoForm()
    if form.validate_on_submit():
        nuevo_alumno = Alumno(
            nombre=form.nombre.data,
            apellido_paterno=form.apellido_paterno.data,
            apellido_materno=form.apellido_materno.data,
            fecha_nacimiento=str(form.fecha_nacimiento.data),
            grupo=form.grupo.data
        )
        db.session.add(nuevo_alumno)
        db.session.commit()
        flash('Alumno registrado exitosamente', 'success')
        return redirect(url_for('alumno'))
    return render_template('alumno.html', form=form)

@app.route('/crear_examen', methods=['GET', 'POST'])
def crear_examen():
    form = PreguntaForm()
    if request.method == 'POST':
        pregunta = request.form.get('pregunta')
        opcion_a = request.form.get('opcion_a')
        opcion_b = request.form.get('opcion_b')
        opcion_c = request.form.get('opcion_c')
        opcion_d = request.form.get('opcion_d')
        respuesta_correcta = request.form.get('respuesta_correcta')

        nueva_pregunta = Pregunta(
            pregunta=pregunta,
            opcion_a=opcion_a,
            opcion_b=opcion_b,
            opcion_c=opcion_c,
            opcion_d=opcion_d,
            respuesta_correcta=respuesta_correcta
        )
        db.session.add(nueva_pregunta)
        db.session.commit()
        flash('Pregunta agregada exitosamente', 'success')
        return redirect(url_for('crear_examen'))
    return render_template('crear_examen.html',form=form)

@app.route('/realizar_examen', methods=['GET', 'POST'])
def realizar_examen():
    create_form = forms.AlumnoForm(request.form)
    alumno = None
    mensaje_error = None
    preguntas = Pregunta.query.all()
    edad = None
    if request.method == 'POST':
        if 'buscar_alumno' in request.form:
            nombre = request.form.get('nombre')
            apellido_paterno = request.form.get('apellido_paterno')
            alumno = Alumno.query.filter_by(nombre=nombre, apellido_paterno=apellido_paterno).first()
            if alumno:
                fecha_nacimiento = datetime.datetime.strptime(alumno.fecha_nacimiento, '%Y-%m-%d')
                hoy = datetime.datetime.now()
                edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            else:
                mensaje_error = 'Alumno no encontrado'
        elif 'guardar_examen' in request.form:
            alumno_id = request.form.get("alumno_id")  
            if alumno_id:  
                alumno = Alumno.query.get(alumno_id)  
                if alumno:
                    respuestas_guardadas = False 
                    for pregunta in preguntas:
                        respuesta_alumno = request.form.get(f'pregunta_{pregunta.id}')
                        if respuesta_alumno in ['A', 'B', 'C', 'D']: 
                            nueva_respuesta = Respuesta(
                                alumno_id=alumno.id,
                                pregunta_id=pregunta.id,
                                respuesta_alumno=respuesta_alumno
                            )
                            db.session.add(nueva_respuesta)
                            respuestas_guardadas = True  
                    if respuestas_guardadas:
                        db.session.commit()
                        flash("Examen guardado correctamente", "success")
                    else:
                        flash("No se registraron respuestas válidas", "error")
                    return redirect(url_for('calificaciones'))
                else:
                    flash('Alumno no encontrado', 'error')
    return render_template('realizar_examen.html', alumno=alumno, mensaje_error=mensaje_error, preguntas=preguntas, edad=edad, form=create_form)



@app.route('/calificaciones', methods=['GET', 'POST'])
def calificaciones():
    form = GrupoForm()
    grupos = db.session.query(Alumno.grupo).filter(Alumno.grupo.isnot(None)).distinct().all()
    grupos = [grupo[0] for grupo in grupos]
    form.grupo.choices = [(grupo, grupo) for grupo in grupos]
    calificaciones = None
    grupo_seleccionado = None
    if form.validate_on_submit():
        grupo_seleccionado = form.grupo.data
        alumnos_grupo = Alumno.query.filter_by(grupo=grupo_seleccionado).all()
        if alumnos_grupo:
            calificaciones = []
            for alumno in alumnos_grupo:
                respuestas_alumno = Respuesta.query.filter_by(alumno_id=alumno.id).all()  # <-- Corregido aquí
                if respuestas_alumno:
                    calificacion = sum(
                        1 for respuesta in respuestas_alumno
                        if Pregunta.query.get(respuesta.pregunta_id).respuesta_correcta == respuesta.respuesta_alumno
                    )
                    calificacion_promedio = (calificacion / len(respuestas_alumno)) * 10
                    calificaciones.append({
                        'nombre_alumno': f'{alumno.nombre} {alumno.apellido_paterno} {alumno.apellido_materno}',
                        'calificacion': f'{calificacion_promedio:.2f}'
                    })
                else:
                    calificaciones.append({
                        'nombre_alumno': f'{alumno.nombre} {alumno.apellido_paterno} {alumno.apellido_materno}',
                        'calificacion': '0.00'
                    })
    return render_template('calificaciones.html', form=form, calificaciones=calificaciones, grupo_seleccionado=grupo_seleccionado)

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)