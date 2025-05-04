from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DB = {
    "host": os.environ['DB_HOST'],
    "dbname": os.environ['DB_NAME'],
    "user": os.environ['DB_USER'],
    "password": os.environ['DB_PASS']
}

def get_conn():
    return psycopg2.connect(**DB)

@app.route("/personas", methods=["GET"])
def obtener_personas():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, edad FROM personas")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "nombre": r[1], "edad": r[2]} for r in rows])

@app.route("/personas", methods=["POST"])
def agregar_persona():
    data = request.json
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO personas (nombre, edad) VALUES (%s, %s)", (data["nombre"], data["edad"]))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "ok"})

@app.route("/personas/<int:persona_id>", methods=["PUT"])
def actualizar_persona(persona_id):
    data = request.json
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE personas SET nombre = %s, edad = %s WHERE id = %s", (data["nombre"], data["edad"], persona_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "actualizado"})

# Inicia el servidor de Flask correctamente
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
