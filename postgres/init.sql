CREATE TABLE etl_data (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    calificacion NUMERIC(3,1) NOT NULL,
    año_lanzamiento INT NOT NULL,
    genero TEXT NOT NULL
);
