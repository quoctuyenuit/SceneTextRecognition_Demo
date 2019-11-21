function open_image_dialog(input) {
	debugger
	var fd = new FormData();
	var files = input.files[0];
	fd.append('file',files);
	$.ajax({
		url: '/upload-image',
		type: 'post',
		data: fd,
		contentType: false,
		processData: false,
		success: function(response){
			debugger
			if (response == 'True') {
				$('#process-container').show();
				$('#input-container').hide();
			}
		},
		error : function(e) {
			debugger
			console.log("ERROR: ", e);
		}
	});

	if (input.files && input.files[0]) {
		var reader = new FileReader();

		reader.onload = function (e) {
			$('#img-process')
				.attr('src', e.target.result);
		};

		reader.readAsDataURL(input.files[0]);
	}

	
}