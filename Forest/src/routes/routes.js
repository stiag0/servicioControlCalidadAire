const express = require('express')
const AppControllers = require('../controllers/controllers')
const router = express.Router()

router.get('/', AppControllers.controller.get_home)
router.get('/get_online_nodes', AppControllers.controller.get_online_nodes)
router.get('/get_offline_nodes', AppControllers.controller.get_offline_nodes)
router.get('/get_predictive_models', AppControllers.controller.get_predictive_models)
router.use(express.urlencoded({ extended: false }));
router.use(express.json());
router.post('/predecir', AppControllers.controller.predecir)
module.exports = router