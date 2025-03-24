#!/usr/bin/env python

import os
import sys
import psycopg2
import glob
from osgeo import ogr
from aux_functions import *
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv, dotenv_values

irregular_regions_folder             = './irregular_regions'
create_base_irregular_table           = './sql/create_base_irregular_table.sql'
insert_irregular_shapefile           = './sql/insert_irregular_shapefile.sql' 
create_smallgeom_table     = './sql/create_indexandsimplifiedgeom_table.sql'

create_materialized_view = './sql/geojson_irregular_views.sql'
populate_materialized_view   = './sql/irregular_geojson_row.sql' # analisis ok

aoi_file                 = './irregular_regions/sub_aoi.txt'

create_catgrid           = './sql/create_catgrid.sql'
insert_catgrid_record    = './sql/insert_catgrid_record.sql'

create_cat_footprintregion_table = './sql/create_cat_footprintregion_table.sql'
insert_cat_footprintregion = './sql/insert_cat_footprintregion.sql'


logger = setup_logger()
load_dotenv() 

DBNICHENAME=os.getenv("DBNICHENAME")
DBNICHEHOST=os.getenv("DBNICHEHOST")
DBNICHEPORT=os.getenv("DBNICHEPORT")
DBNICHEUSER=os.getenv("DBNICHEUSER")
DBNICHEPASSWD=os.getenv("DBNICHEPASSWD")


class ShapeFileConfig:
  def __init__(self, filename, filepath, srid, resolution, status, clave_namecol, nombre_namecol, clave_enlace_namecol, encoding='utf-8'):
    self.filename = filename            # Nombre de referencia del shape
    self.filepath = filepath    # Ruta al archivo .shp
    self.srid = srid            # Código EPSG del sistema de referencia
    self.encoding = encoding    # Codificación de caracteres (opcional)
    self.clave_namecol = clave_namecol # nombre de la clave en el archivo shape
    self.nombre_namecol = nombre_namecol # nombre del nombre en el archivo shape
    self.clave_enlace_namecol = clave_enlace_namecol # nombre de la clave para enlazar otro shape en el archivo shape
    self.resolution = resolution # resolucion del shape
    self.status = status # estatus del shape, si esta activo o inactivo

  def __repr__(self):
    return f"<ShapeFileConfig filename='{self.filename}' filepath='{self.filepath}' srid='{self.srid}' resolution='{self.resolution}' status='{self.status}' clave_namecol={self.cve_name} nombre_namecol={self.nombre_namecol} clave_enlace_namecol={self.clave_enlace_namecol} >"

# lista de shapes a cargar
shapes = [
  ShapeFileConfig(
          filename='estados.shp',
          filepath=irregular_regions_folder+'/estados.shp',
          srid=32614,
          clave_namecol='CVEGEO',
          nombre_namecol='nombre',
          clave_enlace_namecol=None,
          resolution='state',
          status=True
      ),
  ShapeFileConfig(
          filename='municipios.shp',
          filepath=irregular_regions_folder+'/municipios.shp',
          srid=32614,
          clave_namecol='CVEGEO',
          nombre_namecol='nombre',
          clave_enlace_namecol='clave_enla',
          resolution='mun',
          status=True
      ),
  ShapeFileConfig(
          filename='agebs.shp',
          filepath=irregular_regions_folder+'/agebs.shp',
          srid=32614,
          clave_namecol='CVEGEO',
          nombre_namecol='nombre',
          clave_enlace_namecol='clave_enla',
          resolution='ageb',
          status=True
      ),
  ShapeFileConfig(
          filename='cuencasmx.shp',
          filepath=irregular_regions_folder+'/cuencasmx.shp',
          srid=32614,
          clave_namecol='clave',
          nombre_namecol='nombre',
          clave_enlace_namecol='clave_enla',
          resolution='cue',
          status=True
      )
]


# # Obteniendo variables de ambiente
# try:

#     logger.info('lectura de USUARIO: {0} en el HOST: {1} y PUERTO: {2}'.format(DBNICHEUSER, DBNICHEHOST, DBNICHEPORT))
# except Exception as e:
#     logger.error('No se pudieron obtener las variables de entorno requeridas : {0}'.format(str(e)))
#     sys.exit()


logger.info('Preparando creacion de tablas base de mallas irregulares en DB {0}'.format(DBNICHENAME))
try:
  conn = psycopg2.connect('dbname={0} host={1} port={2} user={3} password={4}'.format(DBNICHENAME, DBNICHEHOST, DBNICHEPORT, DBNICHEUSER, DBNICHEPASSWD))
  conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
  cur = conn.cursor()

  for shape in shapes:
    
    if shape.status == False:
      logger.info('shape descartado: {0}'.format(shape.filename))
      continue

    create_base_irregular_table_sql = get_sql(create_base_irregular_table).format(resolution=shape.resolution)
    logger.info('Creando malla irregular %s', shape.resolution)
    cur.execute(create_base_irregular_table_sql)

except Exception as e:
  logger.error('Ocurrio un error en la creacion de tablas base: {0}'.format(str(e)))
  sys.exit()



logger.info('Preparando creacion de mallas irregulares en DB {0} a partir de shapefiles'.format(DBNICHENAME))
try:
  conn = psycopg2.connect('dbname={0} host={1} port={2} user={3} password={4}'.format(DBNICHENAME, DBNICHEHOST, DBNICHEPORT, DBNICHEUSER, DBNICHEPASSWD))
  conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

  cur = conn.cursor()
  
  # os.chdir(irregular_regions_folder)
  # os.chdir('../')

  logger.info('Cargando shapefiles')

  for shape in shapes:

    logger.info('       --> {0}'.format(shape.filename))

    if shape.status == False:
      logger.info('shape descartado: {0}'.format(shape.filename))      
      continue
      
    file = ogr.Open(shape.filepath)
    layer = file.GetLayer(0)

    logger.info('procesando shape %s', file)

    for i in range(layer.GetFeatureCount()):
      feature = layer.GetFeature(i)

      key = feature.GetField(shape.clave_namecol)
      # logger.info('procesando key %s', key)
      
      name = feature.GetField(shape.nombre_namecol)
      # logger.info('procesando name %s', name)
      
      clave_enlace = ''
      if shape.clave_enlace_namecol != None:
        # logger.info('clave_enlace_namecol is not none')
        clave_enlace = feature.GetField(shape.clave_enlace_namecol)
      # logger.info('procesando clave_enlace: %s', clave_enlace)

      wkt = feature.GetGeometryRef().ExportToWkt()
      # logger.info('%s', wkt)

      table = "grid_" + shape.resolution + "_aoi"
      # logger.info('table %s', table)

      insert_irregular_shapefile_sql = get_sql(insert_irregular_shapefile).format(table=table, key=key, name=name, clave_enlace=clave_enlace, wkt=wkt )
      cur.execute(insert_irregular_shapefile_sql)
      
  # os.chdir('../')

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

  for shape in shapes:
    
    if shape.status == False:
      logger.info('shape descartado: {0}'.format(shape.filename))      
      continue

    create_smallgeom_table_sql = get_sql(create_smallgeom_table).format(resolution=shape.resolution)
    logger.info('Creando small geom para tabla irregular %s', shape.resolution)
    cur.execute(create_smallgeom_table_sql)

except Exception as e:
  logger.error('Ocurrio un error en la creacion de tablas base: {0}'.format(str(e)))
  sys.exit()



logger.info('Preparando creacion de materialized views en DB {0}'.format(DBNICHENAME))
try:
    conn = psycopg2.connect('dbname={0} host={1} port={2} user={3} password={4}'.format(DBNICHENAME, DBNICHEHOST, DBNICHEPORT, DBNICHEUSER, DBNICHEPASSWD))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
    cur = conn.cursor()

    # comentar si se ejecutan primero la construccion de las mallas regulares
    # create_catgrid_sql = get_sql(create_catgrid)
    # cur.execute(create_catgrid_sql)

    # comentar si se ejecutan primero la construccion de las mallas regulares
    # create_cat_footprintregion_table_sql = get_sql(create_cat_footprintregion_table)
    # cur.execute(create_cat_footprintregion_table_sql)


    irregular_regions = get_sql(aoi_file).splitlines()

    logger.info("Construyendo {0} regiones".format(len(irregular_regions)))
    aoiid = 0

    
    # Creando materialized views
    for shape in shapes:
    
        if shape.status == False:
          logger.info('shape descartado: {0}'.format(shape.filename))      
          continue
        
        create_materialized_view_sql = get_sql(create_materialized_view).format(res=shape.resolution)
        aoiid = 1

        for region in irregular_regions:

          insert_cat_footprintregion_sql = get_sql(insert_cat_footprintregion).format(footprint_region=(region))
          cur.execute(insert_cat_footprintregion_sql)
          
          region_id = cur.fetchone()[0] # obtiene el id recien insertado
          logger.info("region_id: {0}".format(region_id))


          countries = region.split(';')
          create_materialized_view_row  = ('' if aoiid == 1 else ' UNION ALL ') + get_sql(populate_materialized_view)
          counid = 1

          # añade contexto de la region
          create_materialized_view_row = create_materialized_view_row.replace('{region_desc}', region)

          for country in countries:
              if counid == 1:
                  create_materialized_view_row = create_materialized_view_row.format(res=shape.resolution, country=country, region_id=region_id)        
              else:
                  where_filter =  "WHERE aoi.country = '{country}' OR"
                  where_filter = where_filter.format(country=country)
                  create_materialized_view_row = create_materialized_view_row.replace('WHERE', where_filter)
              counid += 1

        
          # registro en catalago
          table_view_name = "grid_geojson_" + str(shape.resolution) + "_aoi"
          table_cell_name = "grid_" + str(shape.resolution) + "_aoi"
          insert_catgrid_record_sql = get_sql(insert_catgrid_record).format(region_id=region_id, resolution=shape.resolution, table_view_name=table_view_name, table_cell_name=table_cell_name)
          cur.execute(insert_catgrid_record_sql)

          aoiid += 1
          create_materialized_view_sql += create_materialized_view_row

        # create_materialized_view_sql += get_sql(populate_materialized_view).format(res=res, region_desc= region, region_id=region_id)
        cur.execute(create_materialized_view_sql)
        logger.info('Materialized view de resolucion de {0} creada.'.format(shape.resolution))

    cur.close()
    conn.close()

except Exception as e:
    logger.error('Ocurrio un error en la preparacion y ejecucion de queries de materialized views: {0}'.format(str(e)))
    sys.exit()







