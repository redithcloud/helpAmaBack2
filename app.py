from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Respuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pregunta = db.Column(db.String(180), unique=False)
    valor = db.Column(db.Integer, unique=False)

    def __init__(self, pregunta, valor):
        self.pregunta = pregunta
        self.valor = valor

# Esquema de Respuesta
class RespuestaSchema(ma.Schema):
    class Meta:
        fields = ("pregunta", "valor")

respuesta_schema = RespuestaSchema()
respuestas_schema = RespuestaSchema(many=True)


@app.route("/respuesta", methods=["POST"])
def add_respuesta():
    pregunta = request.json["pregunta"]
    valor = request.json["valor"]

    new_respuesta = Respuesta(pregunta=pregunta, valor=valor)

    db.session.add(new_respuesta)
    db.session.commit()

    respuesta = Respuesta.query.get(new_respuesta.id)

    return respuesta_schema.jsonify(respuesta)

@app.route("/respuesta/<id>" , methods=["GET"])
def get_respuestas(id):
    all_respuestas= Respuesta.query.all()
    result = respuestas_schema.dump(all_respuestas)
    return jsonify(result.data)

@app.route("/respuesta/<id>" , methods=["GET"])
def get_respuesta(id):
    respuesta = Respuesta.query.get(id)
    return respuesta_schema.jsonify(respuesta)

@app.route("/respuesta/<id>" , methods=["PUT"])
def respuesta_update(id):
    respuesta = Respuesta.query.get(id)
    pregunta = request.json["pregunta"]
    valor = request.json["Valor"]

    respuesta.pregunta = pregunta
    respuesta.valor = valor

    db.session.commit()
    return respuesta_schema.jsonify(respuesta)

@app.route("/respuesta/<id>" , methods=["DELTE"])
def respuesta_delete(id):
    respuesta = Respuesta.query.get(id)
    db.session.delete(respuesta)
    db.session.commit()

    return respuesta_schema.jsonify(respuesta)



if __name__ == "__main__":
    app.run(debug=True)
