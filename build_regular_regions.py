#!/usr/bin/env python

import os
import sys
import psycopg2
import glob
from osgeo import ogr
from aux_functions import *
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


DBNICHENAME=''
DBNICHEHOST=''
DBNICHEPORT=0
DBNICHEUSER=''
DBNICHEPASSWD=''

# regions_folder             = './regions'
# regions_folder             = './america_shapes'
regions_folder             = './world_regions'
create_aoi_table           = './sql/create_aoi_table.sql'
insert_shapefile           = './sql/insert_shapefile.sql'
 
create_grid_64km_table     = './sql/create_grid_64km_table.sql'
create_grid_64km_aoi_table     = './sql/create_grid_64km_aoi_table.sql'

create_grid_32km_table     = './sql/create_grid_32km_table.sql'
create_grid_16km_table     = './sql/create_grid_16km_table.sql'
create_grid_8km_table      = './sql/create_grid_8km_table.sql'
create_grid_xxkm_table      = './sql/create_grid_xxkm_table.sql'

aoi_file                 = './regions/sub_aoi.txt'
# aoi_file                 = './regions/world_sub_aoi.txt'
create_materialized_view = './sql/geojson_views.sql'
add_region_view          = './sql/geojson_row.sql' # analisis ok
create_catgrid           = './sql/create_catgrid.sql'
insert_catgrid_record    = './sql/insert_catgrid_record.sql'

logger = setup_logger()

# # Obteniendo variables de ambiente
# try:
#     # DBNICHEHOST, DBNICHEPORT, DBNICHEUSER, DBNICHEPASSWD, DBNICHENAME = reading_environment_vars()

#     logger.info('lectura de USUARIO: {0} en el HOST: {1} y PUERTO: {2}'.format(DBNICHEUSER, DBNICHEHOST, DBNICHEPORT))
# except Exception as e:
#     logger.error('No se pudieron obtener las variables de entorno requeridas : {0}'.format(str(e)))
#     sys.exit()


# # Guardando regiones shapefile y creación de tabla aoi (area of interest), no inserta valores existentes basados en la clave iso a tres digitos
logger.info('Preparando creacion de tabla de países necesaria para creación de mallas y regiones en DB {0}'.format(DBNICHENAME))
try:
  conn = psycopg2.connect('dbname={0} host={1} port={2} user={3} password={4}'.format(DBNICHENAME, DBNICHEHOST, DBNICHEPORT, DBNICHEUSER, DBNICHEPASSWD))
  conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

  cur = conn.cursor()

  create_aoi_table_sql = get_sql(create_aoi_table)
  insert_shapefile_sql = get_sql(insert_shapefile)
  cur.execute(create_aoi_table_sql)

  os.chdir(regions_folder)
    
  logger.info('Cargando shapefiles')
  for filename in glob.glob('*.shp'):
      logger.info('       --> {0}'.format(filename))
      file = ogr.Open(filename)
      layer = file.GetLayer(0)

      fgid = 1
      for i in range(layer.GetFeatureCount()):
          feature = layer.GetFeature(i)
          name = feature.GetField('name') # Poner el nombre de la columna que tiene el nombre del país en el shapefile
          cve_iso = feature.GetField('iso3') # Poner el nombre de la columna que tiene la clave iso a 3 digitos que tiene el shapefile
          continent = feature.GetField('continent') # Se agrega contiente para hacer avances por areas mas extensas
          wkt = feature.GetGeometryRef().ExportToWkt()

          # logger.info('cve_iso: {0}'.format(cve_iso))
          # logger.info('continent: {0}'.format(continent))
          # logger.info('wkt: {0}'.format(wkt))
          # logger.info('name: {0}'.format(name))
          
          if cve_iso is not None:
            cur.execute(insert_shapefile_sql, (fgid, cve_iso, name, continent, wkt, cve_iso))
            fgid += 1

  os.chdir('../')

  cur.close()
  conn.close()

except Exception as e:
  logger.error('No se guardaron todas las regiones: {0}'.format(str(e)))
  sys.exit()



logger.info('Preparando creacion de mallas en DB {0}'.format(DBNICHENAME))
try:
    conn = psycopg2.connect('dbname={0} host={1} port={2} user={3} password={4}'.format(DBNICHENAME, DBNICHEHOST, DBNICHEPORT, DBNICHEUSER, DBNICHEPASSWD))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()
    logger.info('Creación de mallas')

    # ejecutar solo cuando se crea la tabla por primera vez o se desea regenerar la información
    # creación de la tabla base a 64km de todo el mundo (basado en la tabla de aoi, que supone contener todo el mundo)
    # create_grid_64km_table_sql = get_sql(create_grid_64km_table)

    # creacion de tablas del area de interes con base al nivel de area y el valor seleccionado, consultar la tabla de de aoi para revisar valores disponibles a los niveles de continente o país
    create_grid_64km_aoi_table_sql = get_sql(create_grid_64km_aoi_table).format(column_area='continent', value='Americas')  
    create_grid_32km_table_sql = get_sql(create_grid_xxkm_table).format(resolution=32, column_area='country', value='\'Mexico\', \'United States of America\', \'Canada\'') # valores disponibles: column_area: country o continent
    create_grid_16km_table_sql = get_sql(create_grid_xxkm_table).format(resolution=16, column_area='country', value='\'Mexico\', \'United States of America\', \'Canada\'') # valores disponibles: column_area: country o continent
    create_grid_8km_table_sql = get_sql(create_grid_xxkm_table).format(resolution=8, column_area='country', value='\'Mexico\', \'United States of America\', \'Canada\'') # valores disponibles: column_area: country o continent
    
    # ejecutar solo cuando se crea la tabla por primera vez o se desea regenerar la información
    # logger.info('Creando tabla malla de 64km mundial')
    # cur.execute(create_grid_64km_table_sql)

    logger.info('Creando tabla malla de 64km_aoi segun selección')
    cur.execute(create_grid_64km_aoi_table_sql)

    logger.info('Creando tabla malla de 32km segun selección')
    cur.execute(create_grid_32km_table_sql)
    
    logger.info('Creando tabla malla de 16km segun selección')
    cur.execute(create_grid_16km_table_sql)
    
    logger.info('Creando tabla malla de 8km segun selección')
    cur.execute(create_grid_8km_table_sql)

    
    cur.close()
    conn.close()
    logger.info('Se crearon las variables bioticas correctamente')
            
except Exception as err:
    
    logger.error('No se crearon correctamente las variables bioticas: {0}'.format(str(err)))
    err_type, err_obj, traceback = sys.exc_info()
    line_num = traceback.tb_lineno
    print ("\nERROR:", err, "on line number:", line_num)
    print ("traceback:", traceback, "-- type:", err_type)
    sys.exit()



logger.info('Preparando creacion de materialized views en DB {0}'.format(DBNICHENAME))
try:
    conn = psycopg2.connect('dbname={0} host={1} port={2} user={3} password={4}'.format(DBNICHENAME, DBNICHEHOST, DBNICHEPORT, DBNICHEUSER, DBNICHEPASSWD))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
    cur = conn.cursor()

    create_catgrid_sql = get_sql(create_catgrid)
    cur.execute(create_catgrid_sql)

    resolutions = [64, 32, 16, 8]
    # resolutions = [64, 32]

    regions = get_sql(aoi_file).splitlines()

    logger.info("Construyendo {0} regiones".format(len(regions)))
    aoiid = 0
    
    # Creando materialized views
    for res in resolutions:
        
        create_materialized_view_sql = get_sql(create_materialized_view).format(res=res)
        aoiid = 1

        for region in regions:

            logger.info("region: {0}".format(region))

            countries = region.split(';')
            create_materialized_view_row  = ('' if aoiid == 1 else ' UNION ALL ') + get_sql(add_region_view)
            counid = 1

            # añade contexto de la region
            create_materialized_view_row = create_materialized_view_row.replace('{region_desc}', region)

            for country in countries:
                if counid == 1:
                    create_materialized_view_row = create_materialized_view_row.format(res=res, country=country)        
                else:
                    where_filter =  "WHERE aoi.country = '{country}' OR"
                    where_filter = where_filter.format(country=country)
                    create_materialized_view_row = create_materialized_view_row.replace('WHERE', where_filter)
                counid += 1

            # registro en catalago
            table_view_name = "grid_geojson_" + str(res) + "km_aoi"
            insert_catgrid_record_sql = get_sql(insert_catgrid_record).format(footprint_region=aoiid,resolution=res,table_view_name=table_view_name)
            cur.execute(insert_catgrid_record_sql)

            aoiid += 1
            create_materialized_view_sql += create_materialized_view_row
        
        cur.execute(create_materialized_view_sql)
        logger.info('Materialized view de resolucion de {0} km creada.'.format(res))


    cur.close()
    conn.close()
except Exception as e:
    logger.error('Ocurrio un error en la preparacion y ejecucion de queries de materialized views: {0}'.format(str(e)))
    sys.exit()

