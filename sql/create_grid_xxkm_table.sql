-- ** Descomentar SECCION cuando se desea regenerar toda la tabla nuevamente **
DROP TABLE IF EXISTS grid_{resolution}km; 

-- esta tabla contiene una malla que abarca de forma rectangular el territorio del mundo o el abarcado por tabla aoi en conjunto
CREATE TABLE IF NOT EXISTS grid_{resolution}km(gridid_{resolution}km serial PRIMARY KEY,gcol integer,grow integer,geom geometry(POLYGON, 900913));

-- es importante usar la setencia distinct, el algoritmo crea diferentes capas para una columna y una fila
INSERT INTO grid_{resolution}km (geom, gcol, grow) 
SELECT distinct geom, i, j FROM (select (ST_SquareGrid({resolution}000, ST_Transform(geom, 900913))).* from aoi 
	where {column_area} in ({value}) -- agregar solo cuando se requiere acotar, en caso contrario inserta todo el mundo
);

-- ALTER TABLE grid_{resolution}km ADD COLUMN IF NOT EXISTS gridid_{resolution}km serial;
ALTER TABLE grid_{resolution}km ADD COLUMN IF NOT EXISTS the_geom geometry(POLYGON,4326);
UPDATE grid_{resolution}km SET the_geom = ST_Transform(geom,4326);

CREATE INDEX idx_grid_{resolution}km_gridid_{resolution}km ON grid_{resolution}km(gridid_{resolution}km);
CREATE INDEX idx_grid_{resolution}km_the_geom ON grid_{resolution}km USING GIST(the_geom);


-- ** Descomentar solo cuando se desea regenerar toda la tabla nuevamente **
-- DROP TABLE IF EXISTS grid_{resolution}km_aoi;
-- ** Termina Descomentar solo cuando se desea regenerar toda la tabla nuevamente **

-- esta tabla contiene una malla que abarca toda la intersección de la tabla aoi con la malla rectangular de grid_{resolution}km
CREATE TABLE IF NOT EXISTS grid_{resolution}km_aoi(gridid_{resolution}km serial PRIMARY KEY, gcol integer, grow integer, geom geometry(POLYGON, 900913), the_geom geometry(POLYGON, 4326));


INSERT INTO grid_{resolution}km_aoi (gridid_{resolution}km, gcol, grow, geom, the_geom)
SELECT a.gridid_{resolution}km, a.gcol, a.grow, a.geom, a.the_geom 
FROM
	(	SELECT distinct m.gridid_{resolution}km, m.gcol, m.grow, m.geom, m.the_geom 
		FROM grid_{resolution}km AS m 
		JOIN aoi AS a 
		ON st_intersects(a.geom, m.the_geom) 
		WHERE {column_area} in ({value})
	) AS a
WHERE NOT EXISTS ( 
	SELECT 1 
	FROM grid_{resolution}km_aoi as b WHERE b.gridid_{resolution}km = a.gridid_{resolution}km
);


DROP INDEX IF EXISTS idx_grid_{resolution}km_aoi_gridid_{resolution}km;
DROP INDEX IF EXISTS idx_grid_{resolution}km_aoi_the_geom;

CREATE INDEX idx_grid_{resolution}km_aoi_gridid_{resolution}km ON grid_{resolution}km_aoi(gridid_{resolution}km);
CREATE INDEX idx_grid_{resolution}km_aoi_the_geom ON grid_{resolution}km_aoi USING GIST(the_geom);

-- se elimina tabla base
DROP TABLE IF EXISTS grid_{resolution}km; 


