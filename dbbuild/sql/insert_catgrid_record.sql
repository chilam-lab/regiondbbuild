INSERT INTO cat_grid(region_id, resolution, table_view_name)
SELECT '{footprint_region}', '{resolution}', '{table_view_name}' 
WHERE NOT EXISTS ( SELECT 1 FROM cat_grid WHERE region_id = '{footprint_region}' and resolution = '{resolution}');