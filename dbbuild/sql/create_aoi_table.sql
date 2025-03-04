DROP MATERIALIZED VIEW IF EXISTS grid_geojson_64km_aoi;
DROP MATERIALIZED VIEW IF EXISTS grid_geojson_32km_aoi;
DROP MATERIALIZED VIEW IF EXISTS grid_geojson_16km_aoi;
DROP MATERIALIZED VIEW IF EXISTS grid_geojson_8km_aoi;
DROP MATERIALIZED VIEW IF EXISTS grid_geojson_statekm_aoi;
DROP MATERIALIZED VIEW IF EXISTS grid_geojson_munkm_aoi;
DROP MATERIALIZED VIEW IF EXISTS grid_geojson_agebkm_aoi;
DROP MATERIALIZED VIEW IF EXISTS grid_geojson_cuekm_aoi;

DROP TABLE IF EXISTS aoi;

CREATE TABLE IF NOT EXISTS aoi(aoi_id serial, fgid integer, cve_iso varchar(3), country varchar(200), continent varchar(200), geom geometry(MultiPolygon, 4326));