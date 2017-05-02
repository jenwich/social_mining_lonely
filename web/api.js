var MongoClient = require('mongodb').MongoClient
var secret = require('./secret')
var fs = require('fs')
var path = require('path')
var moment = require('moment')

var url = `mongodb://${secret.MONGODB_USERNAME}:${secret.MONGODB_PASSWORD}@${secret.MONGODB_HOST}:${secret.MONGODB_PORT}/${secret.MONGODB_DATABASE}`

const TOP = 100
const SUGGEST_AMOUNT = 20

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

function calculateScore(friend_coeff, tweet_count) {
  return 120*friend_coeff + 1.2*Math.log(tweet_count)
}

module.exports = {
  getUser: function(screen_name, callback) {
    db.collection('friend_coeff').find({screen_name}).toArray((err, docs) => {
      if (docs.length == 0) {
        callback({error: 'not_found'})
      } else {
        console.log(screen_name, "found user")
        coeffs = docs[0].friend_coeff
        var id = docs[0]._id,
            user_id = docs[0].user_id,
            name = users[id].name
        var users_ = users.map((u, i) => Object.assign({}, u, {
          score: calculateScore(coeffs[i], u.count),
          friend_coeff: coeffs[i]
        }))
        users_ = users_.filter(u => u.user_id != user_id)

        db.collection('user').find({_id: user_id}).toArray((err, docs) => {
          var friends = docs[0].friends
          users_ = users_.filter(u => !friends.includes(u.user_id) && u.user_id != user_id)
            .sort((a, b) => b.score-a.score)
            .slice(0, SUGGEST_AMOUNT)

          db.collection('tweet').find({'user._id': user_id}).toArray((err, docs) => {
            var tweets = docs.map(t => Object.assign({
              text: t.text,
              created_at: moment(t.created_at).format('ddd, DD MMM YYYY HH:mm:ss')
            }))
            //console.log(users_)
            callback({
              name,
              suggests: users_,
              tweets
            })
          })
        })
      }
    })
  },
  getRank: function(callback) {
    var data = users.slice().sort((a, b) => b.count-a.count)
    callback(data.slice(0, TOP))
  }
}
