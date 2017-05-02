var path = require('path')
var express = require('express')
var bodyParser = require('body-parser')
var app = express()

const PORT = 8011

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

app.use('/', express.static(path.join(__dirname, 'public')))
app.use('/api', require('./apiRouter'))

app.listen(PORT, () => console.log("Listening PORT", PORT))


