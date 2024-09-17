-- Funcion usanda en la generacion de la minformacion abiotica
CREATE AGGREGATE aggr_array_cat (anyarray)
(
  sfunc = array_cat,
  stype = anyarray,
  initcond = '{}'
);
