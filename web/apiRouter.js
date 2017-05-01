var router = require('express').Router()
var api = require('./fakeapi')

router.get('/ranking', (req, res) => {
  api.getRank(data => {
    if (data.error) {
      res.status(404).json({
        error: {code:3, text: "ranking error"}
      })
    } else {
      res.json(data)
    }
  })
})

router.get('/user', (req, res) => {
  var screen_name = req.query.screen_name
  if (screen_name) {
    api.getUser(screen_name, data => {
      if (data.error) {
        res.status(404).json({
          error: {code: 2, text: "screen_name \""+ screen_name +"\" not found."} 
        })
      } else {
        res.json(data)
      }
    })
  } else {
    res.status(404).json({
      error: {code: 1, text:"Please specify screen_name."}
    })
  }
})

module.exports = router
