const express = require('express')
const config = require('../config')
const path = require('path')
const app = express()


//settings
app.set('view engine', 'ejs')
app.engine('html', require('ejs').renderFile)

//Middlewares
app.use(express.urlencoded({ extended: false }))

//Routes
app.use(require('./routes/routes'))

//static files
app.use(express.static(path.join(__dirname, 'public')))

app.listen(config.port, ()=> {
    console.log(`Forest App running on http://localhost:${config.port}`)
})