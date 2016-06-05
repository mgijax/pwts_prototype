"use strict";

(function(){

// Create TR
	
// helper for converting form to JSON
$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};
	
function formIsNotEmpty() {
	var fields = $("#trForm").serializeArray();
	
	for (var i=0; i< fields.length; i++) {
		if (fields[i].value != '') {
			return true;
		}
	}
	
	return false;
}
	
function saveForm() {
	
	if (formIsNotEmpty()) {
		
	  $("#message").text("saving TR...");
	  
	  var data = JSON.stringify($("#trForm").serializeObject());
	  console.log(window.TR_CREATE_URL);
	  console.log(data);
	  // do a new request if we have form values
	  $.ajax({
		type: 'POST',
		dataType: "json",
		contentType:"application/json",
		url: window.TR_CREATE_URL,
		data: data
	  }).done(function(response){
		console.log(response);
		var key = response.key
		window.location = window.TR_DETAIL_URL + key;
	  }).fail(function(err){
		$("#message").text(err.responseText || err);
	  });
	}
}
	
$("#trForm").submit(function(e){
	e.preventDefault();
	
	saveForm();
	
	return false;
});

})();