INSERT INTO cat_grid(region_id, resolution, table_view_name)
SELECT '{region_id}', '{resolution}', '{table_view_name}' 
WHERE NOT EXISTS ( SELECT 1 FROM cat_grid WHERE region_id = '{region_id}' and resolution = '{resolution}');