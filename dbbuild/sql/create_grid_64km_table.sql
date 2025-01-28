-- ** Descomentar SECCION cuando se desea regenerar toda la tabla nuevamente **
-- DROP TABLE IF EXISTS grid_64km; 
-- ** Termina Descomentar SECCION cuando se desea regenerar toda la tabla nuevamente **

-- esta tabla contiene una malla que abarca de forma rectangular el territorio del mundo o el abarcado por tabla aoi en conjunto
CREATE TABLE IF NOT EXISTS grid_64km(gridid_64km serial PRIMARY KEY,gcol integer,grow integer,geom geometry(POLYGON, 900913));

-- es importante usar la setencia distinct, el algoritmo crea diferentes capas para una columna y una fila
INSERT INTO grid_64km (geom, gcol, grow) SELECT distinct geom, i, j FROM (select (ST_SquareGrid(64000, ST_Transform(geom, 900913))).* from aoi 
-- where {column_area} = '{value}' -- agregar solo cuando se requiere acotar, en caso contrario inserta todo el mundo
);

-- ALTER TABLE grid_64km ADD COLUMN IF NOT EXISTS gridid_64km serial;
ALTER TABLE grid_64km ADD COLUMN IF NOT EXISTS the_geom geometry(POLYGON,4326);
UPDATE grid_64km SET the_geom = ST_Transform(geom,4326);

DROP INDEX IF EXISTS idx_grid_64km_gridid_64km;
DROP INDEX IF EXISTS idx_grid_64km_the_geom;

CREATE INDEX idx_grid_64km_gridid_64km ON grid_64km(gridid_64km);
CREATE INDEX idx_grid_64km_the_geom ON grid_64km USING GIST(the_geom);