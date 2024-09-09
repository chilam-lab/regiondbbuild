ALTER TABLE grid_{resolution}km_aoi DROP COLUMN IF EXISTS the_geom;

ALTER TABLE grid_{resolution}km_aoi ADD COLUMN the_geom geometry(MULTIPOLYGON,4326);

UPDATE grid_{resolution}km_aoi SET the_geom = ST_Transform(geom,4326);

DROP INDEX IF EXISTS idx_grid_{resolution}km_aoi_the_geom;

CREATE INDEX idx_grid_{resolution}km_aoi_the_geom ON grid_{resolution}km_aoi USING GIST(the_geom);

ALTER TABLE grid_{resolution}km_aoi DROP COLUMN IF EXISTS small_geom;

ALTER TABLE grid_{resolution}km_aoi ADD COLUMN small_geom geometry(MULTIPOLYGON,4326);

-- aprox. se elimina el 50% de los puntos de un poligono (revisar capa en qgis)
UPDATE grid_{resolution}km_aoi SET small_geom = ST_SimplifyPreserveTopology(the_geom, 0.002);

DROP INDEX IF EXISTS idx_grid_{resolution}km_small_geom;

CREATE INDEX idx_grid_{resolution}km_small_geom ON grid_{resolution}km_aoi USING GIST (small_geom);