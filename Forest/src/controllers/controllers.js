const config = require('../../config')
const path = require('path') //This module can work whit directories, this is implemented 'case de difference between linux a windows paths
const fetch = require('node-fetch')
const controller = {}


//Client controllers

controller.get_home = (req, res) => {
    res.render(path.join(config.AppPath, '/src/views/index.html'))  
}

//Internal controllers

controller.predecir = (req, res) => {
    const body = { "model":req.body.metodo, "dia": req.body.dia };

    fetch('http://192.168.10.179:5000/api/predictive_models/run', {
        method: 'post',
        body: JSON.stringify(body),
        headers: { 'Content-Type': 'application/json' }
     })
    .then((res) => {
        console.log(res)
        return res.json()
    })
    .then((json) => {
        let predictions = []
        for( i = 0; i < json.length; ++i) {
            predictions.push(json[i])
        }
        res.send(predictions)
    })
}

controller.get_predictive_models = (req, res) => {
    fetch('http://192.168.10.179:5000/api/predictive_models/available').then((res) => {
        return res.json()
    }).then((json) => {
        let models = []
        for( i = 0; i < json.length; ++i) {
            models.push(json[i])
        }
        res.send(models)
    })
}

controller.get_online_nodes = (req, res) => {   
    fetch('http://siata.gov.co:3000/cc_api/estaciones/listar_minutal/').then((res) => {
        return res.json()
    }).then((json) => {
        let active_nodes = []
        for( i = 0; i < json.length; ++i) {
            if (json[i].online == "Y") {
                active_nodes.push(json[i])
            }
        }
        res.send(active_nodes)
    })
}

controller.get_offline_nodes = (req, res) => {   
    fetch('http://siata.gov.co:3000/cc_api/estaciones/listar_minutal/').then((res) => {
        return res.json()
    }).then((json) => {
        let active_nodes = []
        for( i = 0; i < json.length; ++i) {
            if (json[i].online == "N") {
                active_nodes.push(json[i])
            }
        }
        res.send(active_nodes)
    })
}

module.exports = {
    controller
}