-- ** Descomentar solo cuando se desea regenerar toda la tabla nuevamente **
-- DROP TABLE IF EXISTS grid_64km_aoi;
-- ** Termina Descomentar solo cuando se desea regenerar toda la tabla nuevamente **

-- esta tabla contiene una malla que abarca toda la intersección de la tabla aoi con la malla rectangular de grid_64km
CREATE TABLE IF NOT EXISTS grid_64km_aoi(gridid_64km integer PRIMARY KEY, gcol integer, grow integer, geom geometry(POLYGON, 900913), the_geom geometry(POLYGON, 4326));

INSERT INTO grid_64km_aoi (gridid_64km, gcol, grow, geom, the_geom)
SELECT a.gridid_64km, a.gcol, a.grow, a.geom, a.the_geom 
FROM
	(	SELECT distinct m.gridid_64km, m.gcol, m.grow, m.geom, m.the_geom 
		FROM grid_64km AS m 
		JOIN aoi AS a 
		ON st_intersects(a.geom, m.the_geom) 
		WHERE {column_area} = '{value}'
	) AS a
WHERE NOT EXISTS ( 
	SELECT 1 
	FROM grid_64km_aoi as b WHERE b.gridid_64km = a.gridid_64km
);


DROP INDEX IF EXISTS idx_grid_64km_aoi_gridid_64km;
DROP INDEX IF EXISTS idx_grid_64km_aoi_the_geom;

CREATE INDEX idx_grid_64km_aoi_gridid_64km ON grid_64km_aoi(gridid_64km);
CREATE INDEX idx_grid_64km_aoi_the_geom ON grid_64km_aoi USING GIST(the_geom);





