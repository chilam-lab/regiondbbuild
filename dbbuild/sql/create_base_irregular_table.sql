DROP MATERIALIZED VIEW IF EXISTS grid_geojson_{resolution}_aoi;

DROP TABLE IF EXISTS grid_{resolution}_aoi;

CREATE TABLE IF NOT EXISTS 
grid_{resolution}_aoi(
	gridid_{resolution} serial,
	clave varchar(255) NULL,
	nombre varchar(255) NULL,
	clave_enlace varchar(255) NULL,
	geom geometry(MultiPolygon, 4326) NULL
);

DROP INDEX IF EXISTS idx_grid_{resolution}_aoi_grid_{resolution};

CREATE INDEX idx_grid_{resolution}_aoi_grid_{resolution} ON public.grid_{resolution}_aoi USING btree (gridid_{resolution});