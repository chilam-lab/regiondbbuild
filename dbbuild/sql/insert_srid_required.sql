INSERT INTO spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text)
SELECT 6326, 'EPSG', 6326,
  'GEOGCS["WGS 84", DATUM["WGS_1984", SPHEROID["WGS 84",6378137,298.257223563]], PRIMEM["Greenwich",0], UNIT["degree",0.0174532925199433]]',
  '+proj=longlat +datum=WGS84 +no_defs'
WHERE NOT EXISTS (
  SELECT 1 FROM spatial_ref_sys WHERE srid = 6326
);


INSERT INTO spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text)
SELECT 1061, 'EPSG', 1061,
  'GEOGCS["ITRF92", DATUM["D_ITRF92", SPHEROID["GRS 1980",6378137,298.257222101]], PRIMEM["Greenwich",0], UNIT["degree",0.0174532925199433]]',
  '+proj=longlat +ellps=GRS80 +no_defs'
WHERE NOT EXISTS (
  SELECT 1 FROM spatial_ref_sys WHERE srid = 1061
);


INSERT INTO spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text)
SELECT 6372, 'EPSG', 6372,
  'PROJCS["LCC INEGI", GEOGCS["GCS_ITRF92", DATUM["D_ITRF92", SPHEROID["GRS_1980",6378137.0,298.257222101]], PRIMEM["Greenwich",0.0], UNIT["Degree",0.0174532925199433]], PROJECTION["Lambert_Conformal_Conic_2SP"], PARAMETER["standard_parallel_1",17.5], PARAMETER["standard_parallel_2",29.5], PARAMETER["latitude_of_origin",12.0], PARAMETER["central_meridian",-102.0], PARAMETER["false_easting",2500000.0], PARAMETER["false_northing",0.0], UNIT["Meter",1.0]]',
  '+proj=lcc +lat_1=17.5 +lat_2=29.5 +lat_0=12 +lon_0=-102 +x_0=2500000 +y_0=0 +ellps=GRS80 +units=m +no_defs'
WHERE NOT EXISTS (
  SELECT 1 FROM spatial_ref_sys WHERE srid = 6372
);
