-- DROP TABLE IF EXISTS aoi;
CREATE TABLE IF NOT EXISTS aoi(aoi_id serial, fgid integer, cve_iso varchar(3), country varchar(200), continent varchar(200), geom geometry(MultiPolygon, 4326));