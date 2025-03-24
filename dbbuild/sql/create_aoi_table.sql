DROP MATERIALIZED VIEW IF EXISTS grid_geojson_64km_aoi;
DROP MATERIALIZED VIEW IF EXISTS grid_geojson_32km_aoi;
DROP MATERIALIZED VIEW IF EXISTS grid_geojson_16km_aoi;
DROP MATERIALIZED VIEW IF EXISTS grid_geojson_8km_aoi;
DROP MATERIALIZED VIEW IF EXISTS grid_geojson_state_aoi;
DROP MATERIALIZED VIEW IF EXISTS grid_geojson_mun_aoi;
DROP MATERIALIZED VIEW IF EXISTS grid_geojson_ageb_aoi;
DROP MATERIALIZED VIEW IF EXISTS grid_geojson_cue_aoi;


DROP TABLE IF EXISTS aoi;

CREATE TABLE IF NOT EXISTS aoi(aoi_id serial, fgid integer, cve_iso varchar(3), country varchar(200), continent varchar(200), geom geometry(MultiPolygon, 4326));