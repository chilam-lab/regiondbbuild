INSERT INTO cat_grid(footprint_region, resolution, table_view_name)
SELECT '{footprint_region}', '{resolution}', '{table_view_name}' 
WHERE NOT EXISTS ( SELECT 1 FROM cat_grid WHERE footprint_region = '{footprint_region}' and resolution = '{resolution}');

