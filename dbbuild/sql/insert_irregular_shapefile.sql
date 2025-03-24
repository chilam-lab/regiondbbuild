INSERT INTO {table}(clave, nombre, clave_enlace, geom)  
VALUES('{key}', '{name}', '{clave_enlace}', ST_Transform( ST_GeometryFromText('{wkt}', 32614), 4326));