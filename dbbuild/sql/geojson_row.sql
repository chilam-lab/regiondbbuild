SELECT {region_id} AS region_id,
  '{region_desc}' as region_description,
	json_build_object(
		'type', 'FeatureCollection',
		'crs',  json_build_object(
  	'type', 'name',
  	'properties', json_build_object(
    	'name', 'urn:ogc:def:crs:EPSG::4326')),
  	'features', json_agg(
    		json_build_object(
      	'type', 'Feature',
    		'geometry', ST_AsGeoJSON(the_geom)::json,
    		'properties', json_build_object(
        		'cellid', gridid_{res}km
      		)
    		)
  		)
		) AS json,
  -- ARRAY( SELECT grid_{res}km_aoi.gridid_{res}km FROM grid_{res}km_aoi LEFT JOIN aoi ON ST_Intersects(grid_{res}km_aoi.the_geom, aoi.geom)
  --     WHERE aoi.country = '{country}'
		-- )::integer[] AS cells,
  -- ST_Envelope(
    ST_Union(
      ARRAY(
        SELECT ST_SimplifyPreserveTopology(aoi.geom, 0.002) FROM aoi 
        WHERE aoi.country='{country}'
        )
    ) as border
  -- ) as border
  -- ARRAY( SELECT gid FROM aoi WHERE country='{country}')::integer[] AS gid
FROM grid_{res}km_aoi LEFT JOIN aoi ON ST_Intersects(grid_{res}km_aoi.the_geom, aoi.geom)
WHERE aoi.country = '{country}'