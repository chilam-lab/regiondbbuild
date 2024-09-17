DROP MATERIALIZED VIEW IF EXISTS grid_geojson_{res}km_aoi;

DROP SEQUENCE IF EXISTS grid_geojson_{res}km_aoi_seq; 

CREATE SEQUENCE grid_geojson_{res}km_aoi_seq;

CREATE MATERIALIZED VIEW grid_geojson_{res}km_aoi AS 