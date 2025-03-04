INSERT INTO cat_grid(region_id, resolution, table_view_name, table_cell_name)
SELECT '{region_id}', '{resolution}', '{table_view_name}', '{table_cell_name}' 
WHERE NOT EXISTS ( SELECT 1 FROM cat_grid WHERE region_id = '{region_id}' and resolution = '{resolution}');