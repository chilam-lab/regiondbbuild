WITH s AS (
    SELECT region_id
    FROM cat_footprintregion
    WHERE footprint_region = '{footprint_region}'
), i as (
    INSERT INTO cat_footprintregion (footprint_region)
    SELECT '{footprint_region}'
    WHERE not exists (
    	SELECT footprint_region 
    	FROM cat_footprintregion as b
    	WHERE b.footprint_region = '{footprint_region}'
    )
    returning region_id
)
SELECT region_id FROM i
UNION ALL
SELECT region_id FROM s