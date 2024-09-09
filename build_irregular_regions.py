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

irregular_regions_folder             = './irregular_regions'
create_base_irregular_table           = './sql/create_base_irregular_table.sql'
insert_irregular_shapefile           = '../sql/insert_irregular_shapefile.sql' 
create_smallgeom_table     = './sql/create_indexandsimplifiedgeom_table.sql'

create_materialized_view = './sql/geojson_views.sql'
populate_materialized_view   = './sql/irregular_geojson_row.sql' # analisis ok

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


logger.info('Preparando creacion de tablas base de mallas irregulares en DB {0}'.format(DBNICHENAME))
try:
  conn = psycopg2.connect('dbname={0} host={1} port={2} user={3} password={4}'.format(DBNICHENAME, DBNICHEHOST, DBNICHEPORT, DBNICHEUSER, DBNICHEPASSWD))
  conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
  cur = conn.cursor()

  # resolutions = ["cue"]
  resolutions = ["state", "mun", "ageb", "cue"]

  for res in resolutions:
    create_base_irregular_table_sql = get_sql(create_base_irregular_table).format(resolution=res)
    logger.info('Creando malla irregular %s', res)
    cur.execute(create_base_irregular_table_sql)

except Exception as e:
  logger.error('Ocurrio un error en la creacion de tablas base: {0}'.format(str(e)))
  sys.exit()



logger.info('Preparando creacion de mallas irregulares en DB {0} a partir de shapefiles'.format(DBNICHENAME))
try:
  conn = psycopg2.connect('dbname={0} host={1} port={2} user={3} password={4}'.format(DBNICHENAME, DBNICHEHOST, DBNICHEPORT, DBNICHEUSER, DBNICHEPASSWD))
  conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

  cur = conn.cursor()
  
  os.chdir(irregular_regions_folder)
    
  logger.info('Cargando shapefiles')

  # relaciones entre shapes y clave capas
  irregular_map = {}
  irregular_map["estados.shp"] = "state"
  irregular_map["municipios.shp"] = "mun"
  irregular_map["agebs.shp"] = "ageb"
  irregular_map["cuencasmx.shp"] = "cue"


  for filename in glob.glob('*.shp'):
    logger.info('       --> {0}'.format(filename))
    file = ogr.Open(filename)
    layer = file.GetLayer(0)

    logger.info('procesando shape %s', file)

    for i in range(layer.GetFeatureCount()):
      feature = layer.GetFeature(i)

      key = feature.GetField('clave')
      # logger.info('procesando key %s', key)

      name = feature.GetField('nombre')
      # logger.info('procesando name %s', name)

      if filename == "estados.shp":
        # se requiere para todos los shapes excepto el base (ej: estados)
        clave_enlace = ''
      else:
        clave_enlace = feature.GetField('clave_enla')
        # logger.info('procesando clave_enlace %s', clave_enlace)

      wkt = feature.GetGeometryRef().ExportToWkt()
      # logger.info('%s', wkt)

      table = "grid_" + irregular_map.get(filename) + "km_aoi"
      # logger.info('table %s', table)

      insert_irregular_shapefile_sql = get_sql(insert_irregular_shapefile).format(table=table, key=key, name=name, clave_enlace=clave_enlace, wkt=wkt )
      cur.execute(insert_irregular_shapefile_sql)
      
  os.chdir('../')

  cur.close()
  conn.close()

except Exception as e:
  logger.error('No se guardaron todas las regiones: {0}'.format(str(e)))
  sys.exit()


logger.info('Preparando creacion de columnas small geom para mallas irregulares en DB {0}'.format(DBNICHENAME))
try:
  conn = psycopg2.connect('dbname={0} host={1} port={2} user={3} password={4}'.format(DBNICHENAME, DBNICHEHOST, DBNICHEPORT, DBNICHEUSER, DBNICHEPASSWD))
  conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
  cur = conn.cursor()

  # resolutions = ["cue"]
  resolutions = ["state", "mun", "ageb", "cue"]

  for res in resolutions:
    create_smallgeom_table_sql = get_sql(create_smallgeom_table).format(resolution=res)
    logger.info('Creando small geom para tabla irregular %s', res)
    cur.execute(create_smallgeom_table_sql)

except Exception as e:
  logger.error('Ocurrio un error en la creacion de tablas base: {0}'.format(str(e)))
  sys.exit()



logger.info('Preparando creacion de materialized views en DB {0}'.format(DBNICHENAME))
try:
    conn = psycopg2.connect('dbname={0} host={1} port={2} user={3} password={4}'.format(DBNICHENAME, DBNICHEHOST, DBNICHEPORT, DBNICHEUSER, DBNICHEPASSWD))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
    cur = conn.cursor()

    create_catgrid_sql = get_sql(create_catgrid)
    cur.execute(create_catgrid_sql)

    resolutions = ["state", "mun", "ageb","cue"]
    # resolutions = ["cue"]
    aoiid = 1
    
    # Creando materialized views
    for res in resolutions:
        
        create_materialized_view_sql = get_sql(create_materialized_view).format(res=res)
        create_materialized_view_sql += get_sql(populate_materialized_view).format(res=res)
        cur.execute(create_materialized_view_sql)

        logger.info('Materialized view de resolucion de {0} km creada.'.format(res))

        # registro en catalago
        table_view_name = "grid_geojson_" + str(res) + "km_aoi"
        insert_catgrid_record_sql = get_sql(insert_catgrid_record).format(footprint_region=aoiid,resolution=res,table_view_name=table_view_name)
        cur.execute(insert_catgrid_record_sql)
        aoiid += 1

    cur.close()
    conn.close()
except Exception as e:
    logger.error('Ocurrio un error en la preparacion y ejecucion de queries de materialized views: {0}'.format(str(e)))
    sys.exit()



