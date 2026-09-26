import os
from flask import Flask, render_template, redirect, url_for, request , flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://app:123qwe@localhost:5432/movies_database'
)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave_super_secreta')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Restaurante(db.Model):
    __tablename__ = 'restaurantes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    ciudad = db.Column(db.String(80), nullable=False)
    direccion = db.Column(db.String(200), nullable=True)
    telefono = db.Column(db.String(30), nullable=True)

    platos = db.relationship('Plato', backref='restaurante', cascade='all, delete-orphan')

class Plato(db.Model):
    __tablename__ = 'platos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    precio = db.Column(db.Numeric(10, 2), db.CheckConstraint('precio > 0'), nullable=False)
    disponible = db.Column(db.Boolean, nullable=False, default=True)

    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurantes.id'), nullable=False)



@app.route('/restaurantes', methods=['GET'])
def listar_restaurantes():
    ciudad_Filtro = request.args.get('ciudad')

    if ciudad_Filtro:
        lista = Restaurante.query.filter(Restaurante.ciudad.ilike(f'%{ciudad_Filtro}%')).all()
    else:
        lista = Restaurante.query.all()

    return render_template('restaurantes/index.html', restaurantes=lista)


@app.route('/restaurantes/<int:restaurante_id>', methods=['GET'])
def detalle_restaurante(restaurante_id):
    restaurante_encontrado = Restaurante.query.get_or_404(restaurante_id)

    return render_template('restaurantes/detalle.html', restaurante=restaurante_encontrado)


@app.route('/restaurantes/<int:restaurante_id>/editar', methods=['GET', 'POST'])
def editar_restaurante(restaurante_id):
    restaurante_encontrado = Restaurante.query.get_or_404(restaurante_id)

    if request.method == 'POST':
        restaurante_encontrado.nombre = request.form.get('nombre')
        restaurante_encontrado.ciudad = request.form.get('ciudad')
        restaurante_encontrado.direccion = request.form.get('direccion')
        restaurante_encontrado.telefono = request.form.get('telefono')

        try:
            db.session.commit()
            flash(f'Sucursal "{restaurante_encontrado.nombre}" actualizado con exito')
            return redirect(url_for('detalle_restaurante', restaurante_id=restaurante_encontrado.id))
        except:
            db.session.rollback()
            flash('Error al actualizar la sucursal.')
            return redirect(url_for('editar_restaurante', restaurante_id=restaurante_encontrado.id))

    return render_template('restaurantes/formulario.html', restaurante= restaurante_encontrado)


##Eliminar sucursal
@app.route('/restaurantes/<int:restaurante_id>/eliminar', methods=['POST'])
def eliminar_restaurante(restaurante_id):
    restaurante_encontrado = Restaurante.query.get_or_404(restaurante_id)

    try:
        db.session.delete(restaurante_encontrado)
        db.session.commit()
        flash(f'sucursal "{restaurante_encontrado.nombre}" eliminado correctamente')
    except:
        db.session.rollback()
        flash('Error al eliminar Sucursal')

    return redirect(url_for('listar_restaurantes'))


@app.route('/restaurantes/<int:restaurante_id>/platos', methods=['POST'])
def agregar_plato(restaurante_id):
    restaurante_encontrado = Restaurante.query.get_or_404(restaurante_id)

    if request.method == 'POST':
        nuevo_nombre_plato = request.form.get('nombre')
        nuevo_precio_plato = request.form.get('precio')

        nuevo_plato = Plato(
            nombre=nuevo_nombre_plato,
            precio=float(nuevo_precio_plato),
            restaurante_id=restaurante_encontrado.id
        )

        try:
            db.session.add(nuevo_plato)
            db.session.commit()
            flash(f'Plato "{nuevo_nombre_plato}" agregando al menu')
        except:
            db.session.rollback()
            flash(f'Error al agregar el plato')

    return redirect(url_for('detalle_restaurante', restaurante_id=restaurante_encontrado.id))

@app.route('/', methods=['GET'])
def inicio():
    return redirect(url_for('listar_restaurantes'))


@app.route('/restaurantes/crear', methods=['GET', 'POST'])
def crear_restaurante():
    if request.method == 'POST':
        nuevo_nombre = request.form.get('nombre')
        nueva_ciudad = request.form.get('ciudad')
        nueva_direccion = request.form.get('direccion')
        nuevo_telefono = request.form.get('telefono')

        nuevo_restaurante = Restaurante(
            nombre=nuevo_nombre,
            ciudad=nueva_ciudad,
            direccion=nueva_direccion,
            telefono=nuevo_telefono
        )

        try:
            db.session.add(nuevo_restaurante)
            db.session.commit()

            flash(f'Sucursal "{nuevo_nombre}" creada con exito')
            return redirect(url_for('listar_restaurantes'))
        except:
            db.session.rollback()
            flash("Error al crear la sucursal. Revisa los datos")
            return redirect(url_for('crear_restaurante'))


    return render_template('restaurantes/formulario.html')


##Manejo de errores
@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('errores/404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('errores/500.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=True)

