-- ** Descomentar SECCION cuando se desea regenerar toda la tabla nuevamente **
DROP TABLE IF EXISTS cat_footprintregion;
-- ** Termina Descomentar SECCION cuando se desea regenerar toda la tabla nuevamente **

CREATE TABLE cat_footprintregion (region_id serial4 NOT NULL, footprint_region varchar(200) NULL);
