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
			"select region_id, resolution, table_view_name from cat_grid cg where grid_id = $<grid_id:raw>", {
				grid_id: grid_id
			}	
		).then(resp => {

			let table_view = resp.table_view_name
			let region_id = resp.region_id

			debug("table_view: " + table_view)
			debug("region_id: " + region_id)

			return t.one(
				"select footprint_region, region_description, \"json\" from $<table_view:raw> where footprint_region = $<region_id:raw>", {
					table_view: table_view,
					region_id: region_id
				}	
			).then(resp => {

				res.status(200).json({
					grid_id: grid_id,
					json: resp.json
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









