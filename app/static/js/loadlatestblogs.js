$(document).ready(function() {
		$.get(
			"/latest_blogs/",
			function(data) { 
				$('#maindiv').html(data); 
			},
			"html"
		);
});

