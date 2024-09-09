INSERT INTO aoi (fgid, cve_iso, country, continent, geom) 
SELECT %s, %s, %s, %s, ST_Multi(ST_GeometryFromText(%s, 4326)) 
WHERE NOT EXISTS ( SELECT 1 FROM aoi WHERE cve_iso = %s);
