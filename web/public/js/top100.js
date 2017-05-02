var API_ROOT = "/api"

$(document).ready(function () {
  $.ajax({
    url: `${API_ROOT}/ranking`,
    success: function(result) {
      $("#ranking").empty();
      var top100 = "";
      for(var i = 0; i < result.length; i++) {
        top100 += friend(result[i], i+1);
      }

      $("#ranking").html(top100);
    }
  });
});

function friend(data, rank) {
	var template = `
        <div class="card">
            <div class="card-block">
              <div class="container">
                <div class="row">
                  <div class="col col-sm-1 col-lg-1">
                    <h1>${rank}</h1>
                  </div>
                  <div class="col col-sm-3 col-lg-2">
                    <img class="card-img img-fluid" src="https://twitter.com/${data['screen_name']}/profile_image?size=original" alt="Card image" height="80" />
                  </div>
                  <div class="col col-sm-7 col-lg-8">
                    <a href="https://twitter.com/${data['screen_name']}"><h3 class="card-title">${data['name']}</h3></a>
                    <h4 class="card-subtitle">@${data['screen_name']}</h4>
                  </div>
                </div>
              </div>
            </div>
        </div>
        <br />
	`;
	return template;
}
