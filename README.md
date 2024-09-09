# Repositorio para la creación de mallas y regiones para el proyecto SPECIES y Conexiones.

> Rev. 1.1

## Resumen

Este repositorio contiene los scripts para la creacion de la base de datos que contiene las tablas y vistas utilizadas en el proyecto de SPECIES y proyectos relacionados (EPI-SPECIES, EPI-PUMA, entre otros). Los scripts de este repositorio, buscan la estadarización para el consumo de las mallas y regiones que establecen la coocurrencia geográfica de las diversas variables que existen en los proyectos actuales y posbiles proyectos futuros.


## Datos resultantes de la ejecución de scripts

Las tablas que son creadas por estos scripts se componen de la siguiente manera:

- Tablas que representan mallas en diferentes resoluciones, ya sean regulares o irregulares, llamados grids.
- Vistas meterializadas que son regiones o subregiones de los grids, por tanto, estan sujetos a la resolución base del grid con el cual fue creado. Se disponibilizan en formato geojson.
- Tabla catalago de las vistas (region-resolución) disponibles.

Para el consumo de las mallas y vistas, se realizará la implementación de servicios web que disponibilizaran la información de forma estadarizada y accesible para cualquier proyecto que las requiera.

## Información requerida para la creación de mallas y vistas por medio de los scripts

Para la generación de las mallas y vistas es necesario descargar las fuentes de datos necesarias, los scripts parten del hecho, que esta información estará en formato shapefile. A continuación, se comparten las ligas de los shapesfiles con los cuales ya han sido generadas las mallas y vistas necesarias para el proyecto de SPECIES. (En caso de ya no estar vigente laliga, buscar un shapefile alternativo)

### Ligas shapefiles

- Shapefile para la creación de malla mundial. Necesaria para la creación de mallas regulares. https://public.opendatasoft.com/explore/dataset/world-administrative-boundaries/export/
- Shapefile para la creación de malla de Estados de México. Necesaria para la creación de mallas irregulares. http://geoportal.conabio.gob.mx/metadatos/doc/html/dest_2010gw.html
- Shapefile para la creación de malla de Municipios de México. Necesaria para la creación de mallas irregulares. http://geoportal.conabio.gob.mx/metadatos/doc/html/muni_2018gw.html
- Shapefile para la creación de malla de Cuencas de México. Necesaria para la creación de mallas irregulares. http://geoportal.conabio.gob.mx/metadatos/doc/html/cuencasmx.html
- Shapefile para la creación de malla de AGEBs de México. Necesaria para la creación de mallas irregulares.


## Preparación de información para la construcción de la base de datos

Para ejecutar las operaciones espaciales y la creación de algunos indices de forma correcta, es necesario ejecutar las setencias que vienen en el archivo de create_extensiones.sql

Para generar las mallas regulares en las diferentes resoluciones, es necesario, estadarizar los atributos del shapefile mundial, para que contengan los atributos name, iso3 y continent que son necesarios para la creación de la tabla base de regiones (tablao aoi). Esta edición se puede hacer desde cualquier GIS, como QGIS. Los shapefiles deben ir divididos por país dentro de la carpeta de regions.

De la misma forma, para generar las mallas irregulares en las diferentes resoluciones, es necesario, estadarizar los atributos de los shapefile, para que contengan los atributos clave, nombre y clave_enla, donde clave_enla es la clave para relacionar los municipios, con los estados y los agebs con los municipios. Esta edición se puede hacer desde cualquier GIS, como QGIS. Los shapefiles deben ir dentro de la carpeta de irregular_regions.

Se recomienda ejecutar primeramente el script de las capas regulares, build_regular_regions.py, el cual generara las mallas y las vistas de las resoluciones 64, 32, 16 y 8 kilometros. Es importante acotar las áreas geográficas en la sección "Preparando creacion de mallas en DB". Donde se permite configurar el área a cubrir por continente o por país. 

En el paso previó "Preparando creacion de tabla de países necesaria para creación de mallas y regiones en DB", se contruye la tabla aoi, la cual nos muestra los valores que se pueden configurar en el área. Los scripts son escalables y no repetitivos en el incremento de áreas, por tanto, se puede ir extendiendo el área en medida de las necesidades de los proyectos.

Despues de que las mallas y vistas ha sido creada, es necesario ejecutar el script build_regular_irreregions.sql, este script esta configurado para insertar las resoluciones de estados, municipios, agebs y cuencas de México. Por tanto, no requiere mayor configuración además de la mencionada en un inicio.

Ambos scripts, cada que es creada una vista, realiza una inserción en la tabla de catalogo, la cual servira como base para el servicio a desarrollar, que mostrará las regiones y resoluciones disponibles.