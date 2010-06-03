$(document).ready(function() {
		$.get(
			"/latest_blogs/",
			function(data) { 
				$('#latestBlogs').html(data); 
			},
			"html"
		);
});

