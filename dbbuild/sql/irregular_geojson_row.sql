SELECT {footprint_region} AS footprint_region,
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
        		'cellid', gridid_{res}km
      		)
    		)
  		)
		) AS json,  
  -- ST_Envelope(
    ST_Union(
      ARRAY(
        SELECT small_geom FROM grid_{res}km_aoi 
        )
    -- )
    ) as border
FROM grid_{res}km_aoi