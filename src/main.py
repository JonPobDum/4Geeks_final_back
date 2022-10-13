"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, render_template
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime 
from werkzeug.security import generate_password_hash, check_password_hash
#from models import Person

app = Flask(__name__)

jwt = JWTManager(app) # INICIALIZANDO LA APLICACIÓN QUE TRABAJARA CON FLASK JWT------------------

app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)




# PARA REGISTRO DE NUEVA CUENTA, DEBO CREAR UN POST-------
#PARA HACER LOGIN NECESITO HACER UN POST.----------
# PARA LOGIN TENGO QUE HACER UN GET  PUT PARA CAMBIAR CONTRASENA--------

#PARA MOSTRAR USUARIOS
@app.route("/user_login", methods=['GET'])
def logeando():
    #todos los usuarios que estan en la base de datos.
    all_user = User.query.all() #traigo todos los usuarios
    print(all_user) #un arreglo de clases
    serializados = list(map(lambda user: user.serialize(), all_user))
    # arreglo.map((ob, index, arreglo)=>(obj.serialize()))
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(serializados)


#REGISTRO NUEVO USUARIO CREADO Y FUNCIONA 
@app.route("/api/register", methods=['POST'])
def registro():

    name = request.json.get("name")
    gender = request.json.get("gender")
    age =request.json.get("age")
    email = request.json.get("email")
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()
    if user: return jsonify({"msg":"email ya esta en uso"}),400

    user=User()
    user.name =name
    user.gender =gender
    user.age =age
    user.email = email
    user.password = generate_password_hash(password)
    user.is_active= True
    user.save()
    # db.session.commit() CONSULTAR SI SE DEJA PARA PODER MANTENER LOS CAMBIOS

    return jsonify({"msg":"usuario registrado, por favor inicie session"}), 201



#PARA VER EL PERFIL DEL USUARIO ªªªªno funcionaºººººººº consultar
@app.route("/perfil/<user_name>", methods=['GET'])
def one_user(user_name):
    one = name.query.filter_by(name=user_name).first
    print(one)
    return jsonify(one.serialize())



#----TOKEN PARA LOGIN------
#SE INSTALO PIPENV INSTALL FLASK-JWT-EXTENDED----------------
#SE REALIZO IMPORTACIÓN FROM FLASK_JWT_EXTENDED--------------
# create_access_token : para crear token
# jwt_required: sera que la persona tiene permiso para ingresar?-----------
# get_jwt_identity: quien es la persona del token??? ----------------
# datetime: ayuda a concer el tiempo, que hora estamos """"libreria"""""

@app.route("/api/login", methods=['POST'])
def login():
    body = request.get_json()
    one = User.query.filter_by(email =body['email'] ).first()
    if (one is None):
        return "el usuario no existe o los datos son incrrectos"
    else:
        if(check_password_hash(one.password,body["password"])):

            expiracion = datetime.timedelta(seconds= 60)
            acceso = create_access_token(identity = body['email'], expires_delta = expiracion)
            return {
                "login": "ok",
                "token": acceso,
                "tiempo": expiracion.total_seconds()
                # redirect(url_for('login'))
            }
        else: return "la clave es incorrecta, vuelva a intentarlo"

#A ESTA RUTA NO ENTRAS SI NO LE MANDAN UN TOKEN --------------------
@app.route("/perfil", methods = ['GET'])
@jwt_required()
def perfil():
    identidad = get_jwt_identity()
    return " tienes permiso" + identidad


# GET PARA EL USUARIO 











# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
