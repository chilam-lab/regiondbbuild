DROP MATERIALIZED VIEW IF EXISTS grid_geojson_{resolution}km_aoi;

DROP TABLE IF EXISTS grid_{resolution}km_aoi;

CREATE TABLE IF NOT EXISTS 
grid_{resolution}km_aoi(
	gridid_{resolution}km serial,
	clave varchar(255) NULL,
	nombre varchar(255) NULL,
	clave_enlace varchar(255) NULL,
	geom geometry(MultiPolygon, 4326) NULL
);

DROP INDEX IF EXISTS idx_grid_{resolution}km_aoi_grid_{resolution}km;

CREATE INDEX idx_grid_{resolution}km_aoi_grid_{resolution}km ON public.grid_{resolution}km_aoi USING btree (gridid_{resolution}km);