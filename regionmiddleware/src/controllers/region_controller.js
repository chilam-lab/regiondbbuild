var debug = require('debug')('verbs:auth')
var verb_utils = require('./verb_utils')
var pgp = require('pg-promise')()
var config = require('../../config')

var pool = verb_utils.pool 

exports.get_aoi = function(req, res) {

	let { } = req.body;
	pool.any("select aoi_id, cve_iso, country, continent from aoi a", {}).then( 
		function(data) {
			// debug(data);
		res.status(200).json({
			data: data
		})
  	})
  	.catch(error => {
      debug(error)
      res.status(403).json({
      	message: "error al obtener catalogo", 
      	error: error
      })
   	});
}


exports.get_available_views = function(req, res) {

	let { } = req.body;
	pool.any(
		"SELECT grid_id, footprint_region, resolution from cat_grid cg join cat_footprintregion c on cg.region_id = c.region_id order by cg.grid_id", {}).then( 
		function(data) {
		res.status(200).json({
			data: data
		})
  	})
  	.catch(error => {
      debug(error)
      res.status(403).json({
      	message: "error al obtener catalogo", 
      	error: error
      })
   	});
}

exports.get_data_byid = function(req, res) {

	let grid_id = req.params.id
	debug("grid_id: " + grid_id)

	pool.task(t => {

		return t.one(
			"select region_id, resolution, table_view_name, table_cell_name from cat_grid cg where grid_id = $<grid_id:raw>", {
				grid_id: grid_id
			}	
		).then(resp => {

			let table_view = resp.table_view_name
			let region_id = resp.region_id

			debug("table_view: " + table_view)
			debug("region_id: " + region_id)

			return t.one(
				"select region_id, region_description, \"json\", cells from $<table_view:raw> where region_id = $<region_id:raw>", {
					table_view: table_view,
					region_id: region_id
				}	
			).then(resp => {

				res.status(200).json({
					grid_id: grid_id,
					region_description: resp.region_description,
					json: resp.json,
					cells: resp.cells
				})

			}).catch(error => {
		      debug(error)
		      res.status(403).json({
		      	error: "Error al obtener la malla solicitada", 
		      	message: "error al obtener el geojson de la malla solicitada, favor de contactar al administrador"
		      })
		   	})

		}).catch(error => {
	      debug(error)

	      res.status(403).json({	      	
	      	error: "Error al obtener la malla solicitada", 
	      	message: "grid_id de malla no existente, favor de consultar el catalogo de mallas"
	      })
	   	})

	}).catch(error => {
      debug(error)
      res.status(403).json({
      	message: "error general", 
      	error: error
      })
   	});
  	
}


exports.get_cells_byid = function(req, res) {

	let grid_id = req.params.id
	debug("grid_id: " + grid_id)

	pool.task(t => {

		return t.one(
			"select region_id, resolution, table_view_name, table_cell_name from cat_grid cg where grid_id = $<grid_id:raw>", {
				grid_id: grid_id
			}	
		).then(resp => {

			let table_view = resp.table_view_name
			let region_id = resp.region_id

			debug("table_view: " + table_view)
			debug("region_id: " + region_id)

			return t.one(
				"select region_id, region_description, \"json\", cells from $<table_view:raw> where region_id = $<region_id:raw>", {
					table_view: table_view,
					region_id: region_id
				}	
			).then(resp => {

				res.status(200).json({
					grid_id: grid_id,
					region_description: resp.region_description,
					cells: resp.cells
				})

			}).catch(error => {
		      debug(error)
		      res.status(403).json({
		      	error: "Error al obtener la malla solicitada", 
		      	message: "error al obtener el geojson de la malla solicitada, favor de contactar al administrador"
		      })
		   	})

		}).catch(error => {
	      debug(error)

	      res.status(403).json({	      	
	      	error: "Error al obtener la malla solicitada", 
	      	message: "grid_id de malla no existente, favor de consultar el catalogo de mallas"
	      })
	   	})

	}).catch(error => {
      debug(error)
      res.status(403).json({
      	message: "error general", 
      	error: error
      })
   	});
  	
}







exports.gridid_bypoints = function(req, res) {

	let {points} = req.body;

	if(points == null || points.length == 0){
		debug("el arreglo esta vacio")
		return
	}

	let query_temp = ""
	let query_points = ""		

	points.forEach((point, index) => {
				
		if(index==0){
			query_points = query_points + " ST_SetSRID(ST_GeomFromText('" + point + "'), 4326)"	
		}
		else{
			query_points = query_points + ", ST_SetSRID(ST_GeomFromText('" + point + "'), 4326)"
		}
		
	})

	query_temp = `select distinct 
					cg.grid_id, cg.resolution,
					ggka.region_id, region_description 
					from grid_geojson_64km_aoi ggka
					join (
					SELECT unnest(ARRAY[{query_points}]) AS geom_array) as b
					on st_intersects(ggka.border, b.geom_array )
					join cat_grid cg 
					on ggka.region_id = cg.region_id 
					order by cg.grid_id`

	query_temp = query_temp.replace("{query_points}", query_points)

	pool.any(query_temp, {}).then( 
		function(data) {
			// debug(data);
		res.status(200).json({
			data: data
		})
  	})
  	.catch(error => {
      debug(error)
      res.status(403).json({
      	message: "error al obtener catalogo", 
      	error: error
      })
   	});
}









