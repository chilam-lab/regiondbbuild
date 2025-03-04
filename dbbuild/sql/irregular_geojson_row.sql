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
    		'geometry', ST_AsGeoJSON(small_geom)::json,
    		'properties', json_build_object(
        		'cellid', gridid_{res},
            'clave', clave
      		)
    		)
  		)
		) AS json,  
  ARRAY( SELECT clave FROM grid_{res}_aoi LEFT JOIN aoi ON ST_Intersects(grid_{res}_aoi.the_geom, aoi.geom)
      WHERE aoi.country = '{country}'
    )::varchar(50)[] AS cells,
  -- ST_Envelope(
    ST_Union(
      ARRAY(
        SELECT small_geom FROM grid_{res}_aoi 
        )
    -- )
    ) as border
FROM grid_{res}_aoi