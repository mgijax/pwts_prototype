"use strict";

(function(){

// DEBUG TR Details
	
$.ajax({
	dataType: "json",
	url: window.TR_URL
}).done(function(response){
	
	var template = $("#trTemplate").html();
	var rendered = Mustache.render(template, response);
	$("#content").html(rendered);
	console.log(response);
}).fail(function(err){
	$("#content").text(err.responseText || err);
});


})();