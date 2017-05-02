$(document).ready(function () {
	submit_form();
});

var API_ROOT = "http://localhost:8011/api"

function submit_form() {
	$("#form-name").submit(function(e) {
		e.preventDefault();
		var screen_name = $("#ttname").val();

		$.ajax({
			url: `${API_ROOT}/user?screen_name=${screen_name}`,
			success: function(result) {
				$("#header-search").html('<div><hr class="my-4"><h3 style="margin-bottom: 20px">Suggested For You</h3></div>');
				$("#user-profile").html(user_profile(screen_name, result['tweets']));
				$("#suggestfriend-list").empty();
				var suggest_list = "";

				for(var i = 0; i < result['suggests'].length; i++) {
					suggest_list += suggest_friend(result['suggests'][i], i+1);
				}

				$("#suggestfriend-list").html(suggest_list);
			},
			error: function(result) {
				alert("ไม่พบความเหงาใน twitter ของคุณ");
			}
		});
	});
}

function user_profile(screen_name, tweets) {
	var template = `
          <div class="card">
            <div class="card-block">
              <div class="container">
                <div class="row">
                  <div class="col col-sm-4 col-lg-4">
                    <img class="card-img img-fluid" src="https://twitter.com/${screen_name}/profile_image?size=original" alt="Card image" height="80" />
                  </div>
                  <div class="col col-sm-8 col-lg-8">
                  	<a href="https://twitter.com/${screen_name}"><h3 class="card-title">{SCREEN_NAME}</h3></a>
                    <h4 class="card-subtitle">@${screen_name}</h4>
                    <br />`; 
      			for(var i = 0; i < tweets.length; i++) {
                    template += `<p class="card-text"><b>[${tweets[i]['created_at']}]</b> — ${tweets[i]['text']}</p>`;
                }
                template += `
                  </div>
                </div>
              </div>
            </div>
          </div> 
	`;
	return template;
}

function suggest_friend(data, rank) {
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