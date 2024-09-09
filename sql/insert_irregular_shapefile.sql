INSERT INTO {table}(clave, nombre, clave_enlace, geom)  
VALUES('{key}', '{name}', '{clave_enlace}', ST_Multi(ST_GeometryFromText('{wkt}', 4326)));