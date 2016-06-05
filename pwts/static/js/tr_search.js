"use strict";

(function(){

// TR Search
	
function formIsNotEmpty() {
	var fields = $("#searchForm").serializeArray()
	
	for (var i=0; i< fields.length; i++) {
		if (fields[i].value != '') {
			return true;
		}
	}
	
	return false;
}
	
function searchResults() {
	
	if (formIsNotEmpty()) {
		
	  $("#results").text("Searching TRs...");
	  
	  var requestArgs = $("#searchForm").serialize();
	  console.log(requestArgs);
	  // do a new request if we have form values
	  $.ajax({
		dataType: "json",
		url: window.TR_SEARCH_URL + "?" + requestArgs
	  }).done(function(response){
		var template = $("#resultsTemplate").html();
		var rendered = Mustache.render(template, response);
		$("#results").html(rendered);
		console.log(response);
	  }).fail(function(err){
		$("#results").text(err.responseText || err);
	  });
	}
}
	
$("#searchForm").submit(function(e){
	e.preventDefault();
	
	searchResults();
	
	return false;
});

$(function(){
	// attempt search on page load
	searchResults();
});

})();