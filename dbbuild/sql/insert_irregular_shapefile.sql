INSERT INTO {table}(clave, nombre, clave_enlace, geom)
VALUES (
  '{key}',
  '{name}',
  '{clave_enlace}',
  CASE
    WHEN {srid_origen} = 4326 THEN
      ST_SetSRID(ST_GeomFromText('{wkt}'), 4326)
    ELSE
      ST_Transform(ST_SetSRID(ST_GeomFromText('{wkt}'), {srid_origen}), 4326)
  END
);
