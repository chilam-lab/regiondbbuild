DROP MATERIALIZED VIEW IF EXISTS grid_geojson_{res}_aoi;

DROP SEQUENCE IF EXISTS grid_geojson_{res}_aoi_seq; 

CREATE SEQUENCE grid_geojson_{res}_aoi_seq;

CREATE MATERIALIZED VIEW grid_geojson_{res}_aoi AS 