function requestRecognize(data, url) {
    var header = document.getElementById('header-container')

    while (header.lastChild.name == "alert") {
        header.removeChild(header.lastChild);
    }
    $.ajax({
        url: url,
        type: 'post',
        data: data,
        contentType: false,
        processData: false,
        success: function(response){
            debugger
            if (response['status'] == 0) {
                $('#imageResult')
                .attr('src', "#");
                var loader = document.getElementById('loader')
                loader.style.display = "none"
                
                var alert = createAlertPopup('[Lỗi] Tập tin không thể xử lý, vui lòng chọn tập tin khác!')
                header.appendChild(alert)
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
                    iDiv.onmouseover = function() { 
                        iDiv.style.background = "#7d8ba1"
                        mouse_hover(element, true); 
                    }
                    iDiv.onmouseout = function() { 
                        iDiv.style.background = "#F2F2F2"
                        mouse_hover(element, false); 
                    }

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

function createAlertPopup(content) {
    var alert = document.createElement('div');
    alert.name = "alert"
    alert.className = "alert alert-danger alert-dismissible";
    alert.style = "margin-top: 30px;";
    var closeBtn = document.createElement('a');
    closeBtn.className = "close";
    closeBtn.style = "cursor: pointer;";
    closeBtn.setAttribute('data-dismiss', 'alert');
    closeBtn.setAttribute('aria-label', 'close');
    closeBtn.innerHTML = "&times;";

    var contentBox = document.createElement('p');
    contentBox.style = "margin: 0px";
    contentBox.textContent = content;

    alert.appendChild(contentBox);
    alert.appendChild(closeBtn);

    return alert;
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
            var fd = new FormData();
            fd.append('file',input.files[0]);
            requestRecognize(fd, '/upload-image');
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

function submit_url(url) {
    document.getElementById("process-container").style.display = "none";
    document.getElementById("review-container").style.display = "block";
    
    $('#imageResult')
        .attr('src', url);
    
    var loader = document.getElementById('loader')
    loader.style.display = "block"
    var fd = new FormData();
    fd.append('url', url);
    
    requestRecognize(fd, '/upload-url');
}