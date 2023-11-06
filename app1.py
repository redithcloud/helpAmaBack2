from flask import Flask, request, jsonify
import mysql.connector


app = Flask(__name__)

# Configura la conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="Aitzibers-Mac-mini.local",
    user="admin",
    password="Curso1234.",
    database="helpMom"
)
cursor = db.cursor()
@app.route('/guardar_respuestas', methods=['POST'])
def guardar_respuestas():
    try:
        data = request.json  # Suponiendo que las respuestas se envían como JSON
        respuestas = data.get('respuestas')
        print(respuestas)
        # Inserta las respuestas en la tabla respuestasPrueba
        for respuesta in respuestas:
            cursor.execute("INSERT INTO Respuestas (respuesta, valor) VALUES (%s, %s)", (respuesta.respuesta, respuesta.valor))
        db.commit()
        return jsonify({'mensaje': 'Respuestas guardadas con éxito'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/obtener_respuestas', methods=['GET'])
def obtener_respuestas():
    try:
        cursor.execute("SELECT * FROM Respuestas")
        respuestas = cursor.fetchall()
        columnas = [i[0] for i in cursor.description]
        respuestas_dict = [dict(zip(columnas, respuesta)) for respuesta in respuestas]
        return jsonify(respuestas_dict)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

