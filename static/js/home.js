function requestRecognize(file) {
    var fd = new FormData();
    fd.append('file',file);
    $.ajax({
        url: '/upload-image',
        type: 'post',
        data: fd,
        contentType: false,
        processData: false,
        success: function(response){
            debugger

            if (response['status'] == 0) {
                $('#imageResult')
                .attr('src', "#");
                var loader = document.getElementById('loader')
                loader.style.display = "none"

                var alert = document.getElementById('error-alert')
                alert.style.display = 'block'
                var alert_content = document.getElementById('error-content')
                alert_content.textContent = '[Lỗi] Tập tin không thể xử lý, vui lòng chọn tập tin khác!'
            } else {
                // show detected image
                $('#image-processing')
                .attr('src', "data:image/jpeg;charset=utf-8;base64," + response['image']);
                
                // show recognized content
                var result_div = document.getElementById('result');
                
                while (result_div.firstChild) {
                    result_div.removeChild(result_div.firstChild)
                }

                response['strings'].forEach(element => {
                    var para = document.createElement("p");
                    para.style.margin = "0px"
                    var node = document.createTextNode(element);
                    para.appendChild(node);
                    
                    var iDiv = document.createElement('div');
                    iDiv.className = 'box';
                    iDiv.appendChild(para);
                    iDiv.onmouseover = function() { mouse_hover(element, true); }
                    iDiv.onmouseout = function() { mouse_hover(element, false); }

                    result_div.appendChild(iDiv);
                });

                document.getElementById("process-container").style.display = "block";
                document.getElementById("review-container").style.display = "none";
            }
        },
        error : function(e) {
                console.log("ERROR: ", e);
        }
    });
}

function readURL(input) {
	debugger
    if (input.files && input.files[0]) {
        var reader = new FileReader();

	debugger
	reader.onload = function (e) {
            debugger
            document.getElementById("process-container").style.display = "none";
            document.getElementById("review-container").style.display = "block";
            
            $('#imageResult')
                .attr('src', e.target.result);

            var label = document.getElementById('upload-label')
            label.textContent = 'Tập tin: ' + input.files[0].name;
            
            var loader = document.getElementById('loader')
            loader.style.display = "block"

            requestRecognize(input.files[0]);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function mouse_hover(content, isHighLight) {
    debugger
    var fd = new FormData();
    fd.append('content',content);
    fd.append('isHighLight',isHighLight);
    $.ajax({
        url: '/mouse-hover',
        type: 'post',
        data: fd,
        contentType: false,
        processData: false,
        success: function(response){
            debugger
            $('#image-processing')
            .attr('src', "data:image/jpeg;charset=utf-8;base64," + response['image']);
        },
        error: function(e) {
            console.log("ERROR: ", e);
        }
    });
}