from pathlib import Path
import os
from itsdangerous import URLSafeSerializer as Serializer
from flask_mail import Mail, Message
from flask import Flask, render_template, redirect, url_for, flash
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_login import UserMixin, current_user, LoginManager, login_user, login_required, logout_user
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, StatementError
from sqlalchemy import select
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'key'
#configura la sesion para que las cookies solo sean enviadas a traves de conexiones https seguras
app.config['SESSION_COOKIE_SECURE'] = True 
app.config['UPLOAD_FOLDER'] = 'static'

#Configuracion SMTP para el envio del correo de 'reset password'
app.config['MAIL_SERVER'] = 'smtp-relay.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'alexis.correo.de.prueba@gmail.com'
app.config['MAIL_PASSWORD'] = '#Passworddeprueba2024#'
mail = Mail(app)

db = SQLAlchemy(app)
'''creamos un objeto Migrate para poder manejar las migraciones que nos permitan modificar los modelos ya existentes
usando el comando flask db init en consola flask nos ayuda a crear la carpeta migrations junto con todos los archivos y logica
necesarios para poder trabajar con las migraciones'''
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

class Articulo(db.Model):
    __tablename__ = 'articulo'

    id = db.Column(db.Integer, primary_key=True, name='id')
    name = db.Column(db.String(70), unique=True, nullable=False, name='name')
    price = db.Column(db.Float, nullable=False, unique=False, name='price')
    description = db.Column(db.String(250), name='description')
    image_name = db.Column(db.String(250), unique=True, name='image_name')
    #relaciona el articulo a el id de una de las Categorias 
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), name='categoria_id',nullable=False)


class Categorias(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(70), unique=True, nullable=False, name='name')
    image_category = db.Column(db.String(250), unique=True, name='image_category')
    articulos = db.relationship('Articulo', backref='categoria')

class Usuario(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

    def get_token(self):
        serial = Serializer(app.config['SECRET_KEY'])
        return serial.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_token(token):
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return Usuario.query.get(user_id)
    def set_password(self, password):
            self.password =generate_password_hash(password)

    def check_passwored(self, password):
        return check_password_hash(self.password, password)

class UsuarioAdminView(ModelView):
    #apunta a los campos name y password del formulario
    form_columns = ['name', 'password', 'email']

    def on_model_change(self, form, model, is_created):
        if 'password' in form:
            hashed_password = generate_password_hash(form.password.data)
            model.password = hashed_password

# Creamos la clase myadminindexview que hereda de clase adminindexview
class MyAdminIndexView(AdminIndexView):
    #Usando el decorador @login_required sera necesario haber hecho log_in para ingresar a cualquier apartado del panel de administracion
    #incluido el ingreso manual desde la url del navegador
    @login_required
    def is_accessible(self):
        if current_user.is_authenticated:
        # si el login se realizo de manera correcta, usuario_name queda guardado en la sesion y permite ingresar al 
        # panel de admin
            return True

admin = Admin(app, index_view=MyAdminIndexView() ,name='My Admin Panel', template_mode='bootstrap4')
# Agregar los campos de los objetos Articulo y Usuario al panel admin
admin.add_view(ModelView(Articulo, db.session))
admin.add_view(UsuarioAdminView(Usuario, db.session))
admin.add_view(ModelView(Categorias, db.session))

class RegistroForm(FlaskForm):
    user_name = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    email = EmailField('Correo electronico', validators=[DataRequired()])
    submit = SubmitField('Registrar')

# Formulario de login
class LoginForm(FlaskForm):
    user_name = StringField('Nombre de usuario',validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')

# Formulario Password Reset
class ResetPasswordForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Enviar correo")

# Formulario Cambiar Contraseña
class CambiarContraseña(FlaskForm):
    password1 = PasswordField(validators=[DataRequired()])
    password2 = PasswordField(validators=[DataRequired(), EqualTo('password1')] ) 
    submit = SubmitField("Cambiar contraseña")

# Formulario crear articulo
class ArticuloForm(FlaskForm):
    nombre_articulo = StringField('Nombre de articulo', validators=[DataRequired()])
    precio_articulo  = StringField('Precio de articulo', validators=[DataRequired(message="Ingrese un precio válido.")])
    imagen_articulo = FileField('Imagen de articulo', validators=[DataRequired()])
    descripcion_articulo = StringField('Descripcion del articulo', validators=[DataRequired()])
    categorias_articulo = SelectField('Categorias', choices=[])
    submit = SubmitField('Crear articulo')

# Formulario crear categoria
class CategoriaForm(FlaskForm):
    nombre_categoria = StringField('Nombre de articulo', validators=[DataRequired()])
    imagen_categoria = FileField('Imagen de Categoria',validators=[DataRequired()])
    submit = SubmitField('Crear categoria')

@login_manager.user_loader
def load_user(usuario_id):
    return Usuario.query.filter_by(id=int(usuario_id)).first()


def send_email(user):
    token=user.get_token()
    try:
        msg=Message('Password Reset Request', recipients=user.email, sender=app.config['MAIL_USERNAME'])
        msg.body = f'''Para cambiar tu contraseña. Da click en el siguiente enlace
        {url_for('reset_token', token=token, _external=True)}
        '''
        print(msg.body)
        print('a')
    except Exception as e:
        print (e)

@app.route('/') 
def index():
    if current_user.is_authenticated:
        usuario = Usuario.query.get(current_user.id)
        usuario_name = usuario.name
        return render_template('index.html', usuario_name = usuario_name)
    return render_template('index.html')

@app.route('/reset_password/', methods=['GET', 'POST'])
def reset_request():
    form=ResetPasswordForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user:
            send_email(user)
            print("Correo enviado")
    return render_template('reset_password.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = Usuario.verify_token(token)
    if user is None:
        print("Token expirado o invalido, por favor intenta de nuevo")
        return url_for('reset_request')
    form = CambiarContraseña()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password1.data)
        user.password = hashed_password
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('cambiar_contraseña.html', form=form)



@app.route('/crear-articulo', methods=['GET', 'POST'])
@login_required
def articulo_nuevo():
        # Al llamar a la funcion va a crear el formulario dentro de la vista
    form = ArticuloForm()
    form.categorias_articulo.choices = [(categoria.id, categoria.name) for categoria in Categorias.query.all()]
    #validar los datos ingresados en el formulario
    if form.validate_on_submit():
        try:
            # la sintaxis form.nombre,precio,imagen_articulo.data hace referencia a la informacion recuperada 
            # de sus respectivos campos dentro del formulario 
            name = form.nombre_articulo.data
            price = form.precio_articulo.data
            file = form.imagen_articulo.data
            description = form.descripcion_articulo.data
            categoria_id = form.categorias_articulo.data
            #Usa esta variable para guardar el id de la categoria seleccionada en el formulario
            nombre_categoria = Categorias.query.filter(Categorias.id==categoria_id).first()
            #Ruta donde se va a guardar la imagen subida en el formulario "static/'nombre de la categoria'/'nombre de la imagen'"
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], nombre_categoria.name, secure_filename(file.filename)))
            #crea la instancia de articulo
            articulo_creado = Articulo(name=name, price=price, image_name=file.filename, description=description, categoria_id=categoria_id)
            #ejecuta el query y crea el objeto en la base de datos
            db.session.add(articulo_creado)
            
            db.session.commit()
            db.session.close()
            
            flash("El articulo ha sido creado exitosamente")
            return redirect(url_for('articulo_nuevo'))
        except IntegrityError:
            db.session.rollback()
            flash("Error al crear el artículo: El nombre del articulo o de la imagen ya existe")
        except (ValueError,StatementError):
            flash("No puedes ingresar letras en el campo de precio")


    return render_template('crear_productos.html', form=form)

@app.route('/crear-categoria', methods=['GET', 'POST'])
@login_required
def crear_categoria():
    form = CategoriaForm()
    categorias_existentes = Categorias.query.all()
    if form.validate_on_submit():
        try:
            name = form.nombre_categoria.data
            file = form.imagen_categoria.data
            directorio_categoria = os.path.join(os.path.dirname(__file__),'static', name)
            print(Path(__file__))
            print(Path.cwd())
            nombre_imagen = secure_filename(file.filename)
            os.mkdir(directorio_categoria)
            file.save(os.path.join(directorio_categoria, secure_filename(file.filename)))
            categoria_nueva = Categorias(name=name, image_category=nombre_imagen)
            db.session.add(categoria_nueva)
            db.session.commit()
            db.session.close()
            flash('La categoria ha sido creada correctamente')
            return redirect(url_for('crear_categoria'))
        except SQLAlchemyError :
            db.session.rollback()
            flash("La categoria que intentas crear ya existe")
    
    return render_template('crear_categoria.html', form=form, categorias=categorias_existentes)

def actualizar_articulo():
    pass

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/eliminar-articulos')
@login_required
def eliminar_articulos():
    articulos = Articulo.query.all()
    categorias = {}
    for articulo in articulos:
        categoria = Categorias.query.filter_by(id=articulo.categoria_id).first()
        if categoria:
            categorias[articulo.id] = categoria
    print(categorias)
    return render_template('eliminar_productos.html', categorias=categorias, articulos=articulos)

@app.route('/nuestros-productos/')
def nuestros_productos():
    return render_template('nuestros_productos.html', categorias=todas_categorias())

@app.route('/nuestros-productos/<int:categoria_id>')
def productos_categoria(categoria_id):
    categoria = Categorias.query.get_or_404(categoria_id)
    articulos = Articulo.query.filter_by(categoria_id=categoria_id).all()
    return render_template('productos_categoria.html', categoria=categoria, articulos=articulos)

def todos_articulos():
    articulos = Articulo.query.filter_by(categoria_id=Categorias.id).all()
    return articulos

def todas_categorias():
    categorias = Categorias.query.all()
    return categorias

@app.route('/eliminar/<int:articulo_id>')
@login_required
def eliminar_articulo(articulo_id):
    articulo_a_eliminar = Articulo.query.get_or_404(articulo_id)
    imagen_a_eliminar = articulo_a_eliminar.image_name 
    categoria = Categorias.query.filter_by(id=articulo_a_eliminar.categoria_id).first()
    
    path_imagen = Path('app/') / app.config['UPLOAD_FOLDER'] / categoria.name / imagen_a_eliminar
    print(path_imagen)

    try:
        Path.unlink(path_imagen)    
        db.session.delete(articulo_a_eliminar)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "No se pudo eliminar el articulo seleccionado"

@app.route('/registrarse', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    
    if form.validate_on_submit():
        name = form.user_name.data
        email = form.email.data
        hashed_password = generate_password_hash(form.password.data)
        usuario = Usuario(name=name, password=hashed_password, email=email)
        try:
            db.session.add(usuario)
            db.session.commit()
            db.session.close()
            return redirect(url_for('registrarse'))
        except SQLAlchemyError :
            db.session.rollback()
            flash('Los datos ingresados ya existen en la base de datos')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() 
    if form.validate_on_submit():
        #valida el formulario con los datos name, password ingresados en el formulario
        name = form.user_name.data
        password = form.password.data
        #devuelve el primer resultado de usuario filtrado por el campo name, password
        usuario = Usuario.query.filter_by(name=name).first()
        
        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario, remember=False)
            return redirect(url_for('index'))

    if current_user.is_authenticated and current_user.is_active:
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)