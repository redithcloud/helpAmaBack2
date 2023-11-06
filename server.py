from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import logging

app = Flask(__name__)
app.config['DEBUG'] = True
CORS(app)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Curso1234.@127.0.0.1/helpMom'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Configuración del registro
logging.basicConfig(filename='app.log', level=logging.INFO)  # Registra en un archivo llamado 'app.log'

# Definición del modelo de datos
class Respuesta(db.Model):
    __tablename__ = 'Respuestas'
    idRespuestas = db.Column(db.Integer, primary_key=True)
    pregunta1 = db.Column(db.String(255))
    valor1 = db.Column(db.Integer)
    pregunta2 = db.Column(db.String(255))
    valor2 = db.Column(db.Integer)
    # ... añade más campos aquí según sea necesario

@app.route('/respuestas', methods=['POST', 'OPTIONS'])
@cross_origin()
def guardar_respuestas():
    if request.method == 'OPTIONS':
        # Pre-flight request. Reply successfully:
        return jsonify({'status': 'success'}), 200
    elif request.method == 'POST':
        data = request.get_json()

        # Registra la respuesta entrante y otros detalles
        logging.info('Respuesta recibida: %s', data)

        try:
            nueva_respuesta = Respuesta(
                pregunta1=data['pregunta1'],
                valor1=data['valor1'],
                pregunta2=data['pregunta2'],
                valor2=data['valor2'],
                # ... añade más campos aquí según sea necesario
            )
            db.session.add(nueva_respuesta)
            db.session.commit()

            # Registra el éxito de la inserción
            logging.info('Respuesta insertada en la base de datos con ID: %s', nueva_respuesta.idRespuestas)

            return jsonify({'id': nueva_respuesta.idRespuestas}), 201
        except Exception as e:
            # Registra errores si ocurren
            logging.error('Error interno al procesar la solicitud: %s', e)
            return jsonify({'error': 'Error interno al procesar la solicitud'}), 500

if __name__ == '__main__':
    app.run(debug=True)
    with app.app_context():
        db.create_all()
    app.run(port=5000)
