-- ** Descomentar SECCION cuando se desea regenerar toda la tabla nuevamente **
DROP TABLE IF EXISTS cat_grid;
-- ** Termina Descomentar SECCION cuando se desea regenerar toda la tabla nuevamente **

CREATE TABLE IF NOT EXISTS cat_grid (grid_id serial4 NOT NULL,region_id integer NULL,resolution varchar(200) NULL,table_view_name varchar(200) NULL);
