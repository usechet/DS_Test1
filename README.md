# ETL con Docker, Neo4j, PostgreSQL y Traefik

Este proyecto implementa un proceso **ETL (Extract, Transform, Load)** utilizando Docker Compose, Traefik, Neo4j y PostgreSQL. La API REST está desarrollada en **Flask** y expone endpoints para extraer datos de Neo4j, transformarlos y cargarlos en PostgreSQL.

---

## 📌 Requisitos previos

Antes de ejecutar el proyecto, asegúrate de tener instalados:
- **Docker** y **Docker Compose**
- Archivo **`dataset_a_peliculas.csv`** en la carpeta **`data/`**

## 🚀 Pasos para ejecutar el proyecto

### 1️⃣ Crear y levantar los contenedores con Docker Compose

Ejecuta el siguiente comando en la raíz del proyecto:

docker-compose up -d --build


### 2️⃣ Verificar que los contenedores están corriendo

Ejecuta:
docker ps

Debe mostrar los servicios **traefik, neo4j, postgres y etl_service** en ejecución.

### 3️⃣ Cargar el dataset en Neo4j

Abre Neo4j Browser en [http://neo4j.localhost](http://neo4j.localhost) e ingresa la siguiente consulta


LOAD CSV WITH HEADERS FROM 'file:///dataset_a_peliculas.csv' AS row
CREATE (:Pelicula {
    id: row.id,
    nombre: row.nombre,
    calificacion: toFloat(row.calificacion),
    año_lanzamiento: toInteger(row.año_lanzamiento),
    genero: row.genero
});
```

Para verificar la carga, usa:

MATCH (n) RETURN n LIMIT 10;

NEO4J: http://neo4j.localhost/browser/
API:http://localhost/tomas-useche/api/extract

## 🔧 Solución de Problemas

### ❌ "network etl_network not found"

Si la red no existe, créala manualmente:


docker network create etl_network


Luego, conecta los contenedores:


docker ps -q | ForEach-Object { docker network connect etl_network $_ }


### ❌ "ModuleNotFoundError: No module named 'requests'"

Asegúrate de que la imagen de **etl_service** tenga `requests` instalado en **requirements.txt** y vuelve a construir el servicio:


docker-compose up -d --build etl_service


