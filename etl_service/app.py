from flask import Flask, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# 🔹 Configuración de Neo4j (HTTP en lugar de Bolt para Traefik)
NEO4J_URI = "http://test1_usechetomas-neo4j-1:7474/db/neo4j/tx/commit"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "wrongpassword"  
# 🔹 Función para transformar datos
def transformar_pelicula(record):
    nombre_transformado = record["nombre"].lower().replace(" ", "-")

    # Normalizar calificación
    calificacion = float(record["calificacion"])
    if 1 <= calificacion <= 5:
        calificacion_categoria = "Mala"
    elif 5.1 <= calificacion <= 7:
        calificacion_categoria = "Regular"
    else:
        calificacion_categoria = "Buena"

    # Clasificación por décadas
    anio = int(record["anio"])
    decada = (anio // 10) * 10

    # Calcular puntuación ajustada
    puntuacion_ajustada = (calificacion * 2) - ((2025 - anio) / 10)

    return {
        "id": record["id"],
        "nombre": nombre_transformado,
        "calificacion": calificacion,
        "calificacion_categoria": calificacion_categoria,
        "anio": anio,
        "decada": f"{decada}s",
        "genero": record["genero"],
        "puntuacion_ajustada": round(puntuacion_ajustada, 2)
    }

# 🔹 Extraer datos de Neo4j vía HTTP
def obtener_peliculas():
    query = {
        "statements": [{
            "statement": """
                MATCH (p:Pelicula) 
                RETURN p.id AS id, p.nombre AS nombre, p.calificacion AS calificacion, 
                       p.anio_lanzamiento AS anio, p.genero AS genero
            """
        }]
    }

    try:
        response = requests.post(
            NEO4J_URI,
            json=query,
            auth=HTTPBasicAuth(NEO4J_USER, NEO4J_PASSWORD),
            headers={"Content-Type": "application/json"}
        )

        data = response.json()

        # 🔹 Verificar errores en la consulta
        if "errors" in data and data["errors"]:
            return {"error": f"Error en la consulta a Neo4j: {data['errors']}"}

        # 🔹 Extraer datos del resultado
        records = data.get("results", [{}])[0].get("data", [])

        if not records:
            return {"mensaje": "No hay películas en la base de datos"}

        # 🔹 Aplicar transformación a cada película
        return [transformar_pelicula(record["row"]) for record in records]

    except Exception as e:
        return {"error": f"Error en la conexión con Neo4j: {str(e)}"}

# 🔹 Endpoint para extraer y transformar datos
@app.route("/api/extract", methods=["GET"])
def extract():
    peliculas = obtener_peliculas()
    return jsonify(peliculas)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
