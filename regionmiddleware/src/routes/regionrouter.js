
/**
 * Express router que monta las funciones asociadas a redes. 
 * @type {object}
 * @const
 * @namespace netRouter
 */
var router = require('express').Router()
var regionCtrl = require('../controllers/region_controller')

router.all('/', function(req, res) {
  res.json({ 
    data: { 
      message: '¡Yey! Bienvenido al API de Regiones'
    }
  })
})

router.route('/get-aoi')
  .get(regionCtrl.get_aoi)
  .post(regionCtrl.get_aoi)

router.route('/region-grids')
  .get(regionCtrl.get_available_views)
  .post(regionCtrl.get_available_views)

router.route('/region-grids/:id')
  .get(regionCtrl.get_data_byid)
  .post(regionCtrl.get_data_byid)

router.route('/gridid-bypoints')
  .get(regionCtrl.gridid_bypoints)
  .post(regionCtrl.gridid_bypoints)


module.exports = router;