var MongoClient = require('mongodb').MongoClient
var secret = require('./secret')
var fs = require('fs')
var path = require('path')
var moment = require('moment')

var url = `mongodb://${secret.MONGODB_USERNAME}:${secret.MONGODB_PASSWORD}@${secret.MONGODB_HOST}:${secret.MONGODB_PORT}/${secret.MONGODB_DATABASE}`

const TOP = 20

var db, users

function init() {
  MongoClient.connect(url, function(err, db_) {
    if (!err) {
      console.log("Connected successfully to server");
      db = db_

      usersCollection = db.collection('friend_coeff')
      usersCollection.find({}, {friend_coeff: 0}).toArray((err, docs) => {
        users = docs.sort((a, b) => a._id-b._id)

        fs.readFile(path.join(__dirname, 'data', 'count.txt'), (err, data) => {
          var counts = data.toString().split(',').map(i => parseInt(i))
          users.forEach((u, i) => u.count = counts[i])

          fs.readFile(path.join(__dirname, 'data', 'name.txt'), (err, data) => {
            var names = data.toString().split('\n')
            users.forEach((u, i) => u.name = names[i])
            console.log("Ready")
          })
        })
      }) 
    }
  })
}

init()

module.exports = {
  getUser: function(screen_name, callback) {
    db.collection('friend_coeff').find({screen_name}).toArray((err, docs) => {
      if (docs.length == 0) {
        callback({error: 'not_found'})
      } else {
        coeffs = docs[0].friend_coeff
        var id = docs[0]._id,
            user_id = docs[0].user_id
        var users_ = users.map((u, i) => {
          u.score = coeffs[i] + u.count
          return u
        })
        users_ = users_.filter((u, i) => i != id)
        users_ = users_.sort((a, b) => b.score-a.score).slice(0, 20)

        db.collection('tweet').find({'user._id': user_id}).toArray((err, docs) => {
          var tweets = docs.map(t => Object.assign({
            text: t.text,
            created_at: moment(t.created_at).format('ddd, DD MMM YYYY HH:mm:ss')
          }))
          callback({
            suggests: users_,
            tweets
          })
        })
      }
    })
  },
  getRank: function(callback) {
    var data = users.sort((a, b) => b.count-a.count)
    callback(data.slice(0, TOP))
  }
}
