module.exports = {
  getUser: function(screen_name, callback) {
    if (screen_name == 'example') {
      var data = {
        suggests: [
          {id: '1234', screen_name: 'john', name: 'John John', score: 666},
          {id: '5678', screen_name: 'jack', name: 'Jack Jack', score: 999},
        ],
        tweets: [
          {id: '1000', text: 'Hello world', created_at: '1 May 2017'},
          {id: '1001', text: 'Hello is\'s me', created_at: '2 May 2017'},
        ]
      }
      callback(data)
    } else {
      callback({error: 'not_found'})
    }
  },
  getRank: function(callback) {
    var data = [
      {id: '1', screen_name: "mr_lonely", name: "Mr. Lonely", count: 50},
      {id: '2', screen_name: "imhurt", name: "I\'m hurt now", count: 38},
      {id: '3', screen_name: "foreveralone", name: "foreveralone", count: 30},
    ]
    callback(data)
  }
}
