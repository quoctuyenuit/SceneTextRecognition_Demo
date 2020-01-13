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
// ====================================================
// ====================================================
//Upload user input
// ====================================================
function uploadFile(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

	    reader.onload = function (e) {
            document.getElementById("process-container").style.display = "none";
            document.getElementById("review-container").style.display = "block";
            
            var text_review = document.getElementById('review-text')
            text_review.style.display = 'none'
            $('#imageReview')
                .attr('src', e.target.result);

            drawImage(e.target.result);
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

function submit_url(url) {
    document.getElementById("process-container").style.display = "none";
    document.getElementById("review-container").style.display = "block";
    var text_review = document.getElementById('review-text')
    text_review.style.display = 'none'
    
    $('#imageReview')
        .attr('src', url);
    
    drawImage(url);
    var loader = document.getElementById('loader')
    loader.style.display = "block"
    var fd = new FormData();
    fd.append('url', url);
    
    requestRecognize(fd, '/upload-url');
}

function submit_default_img(img_path) {
    document.getElementById("process-container").style.display = "none";
    document.getElementById("review-container").style.display = "block";
    var text_review = document.getElementById('review-text')
    text_review.style.display = 'none'
    
    $('#imageReview')
        .attr('src', img_path);
    
    drawImage(img_path);
    var loader = document.getElementById('loader')
    loader.style.display = "block"
    var fd = new FormData();
    fd.append('img_path', img_path);
    
    requestRecognize(fd, '/upload-default-img');
}
// ====================================================
// ====================================================
//Send request
// ====================================================
function requestRecognize(data, url) {
    var header = document.getElementById('header-container')

    var select_ctrl = document.getElementById('custom-select')
    var selected_value = parseInt(select_ctrl.options[select_ctrl.selectedIndex].value)
    data.append('method', selected_value)
    
    while (header.lastChild.name == "alert") {
        header.removeChild(header.lastChild);
    }
    debugger
    $.ajax({
        url: url,
        type: 'post',
        data: data,
        contentType: false,
        processData: false,
        success: function(response){
            if (response['status'] != 1) {
                $('#imageReview')
                .attr('src', "#");
                var loader = document.getElementById('loader')
                loader.style.display = "none"
                msg = "[Lỗi] Tập tin không thể xử lý, vui lòng chọn tập tin khác!"
                if (response['status'] == 2) {
                    msg = "[Lỗi] Không nhận được phản hồi từ server, vui lòng kiểm tra lại!"
                }
                
                var alert = createAlertPopup(msg)
                header.appendChild(alert)
            } else {
                var blocks = response['blocks'];
                var strings = response['strings'];
                
                blocks = refreshBlocks(blocks);
                drawBBoxes(blocks);

                // show recognized content
                var result_div = document.getElementById('result');
                while (result_div.firstChild) {
                    result_div.removeChild(result_div.firstChild)
                }

                strings.forEach(element => {
                    var para = document.createElement("p");
                    para.style.margin = "0px";
                    var node = document.createTextNode(element);
                    para.appendChild(node);
                    
                    var iDiv = document.createElement('div');
                    iDiv.className = 'box';
                    iDiv.appendChild(para);
                    iDiv.onmouseover = function() { 
                        iDiv.style.background = "#7d8ba1"
                        var index = strings.findIndex(x => { return x == element; });
                        blocks = highLighBlock(blocks, index);
                        drawBBoxes(blocks);
                    }

                    iDiv.onmouseout = function() { 
                        iDiv.style.background = "#F2F2F2"
                        blocks = refreshBlocks(blocks)
                        drawBBoxes(blocks)
                    }

                    result_div.appendChild(iDiv);
                });

                document.getElementById("process-container").style.display = "block";
                document.getElementById("review-container").style.display = "none";
                window.scrollTo(0,document.body.scrollHeight);
            } 

            
            
        },
        error : function(e) {
            console.log("ERROR: ", e);
        }
    });
}
// ====================================================
// ====================================================
//Draw bouding boxes
// ====================================================
var defaultcolor = "#00f54e"
var highlightColor = "#fc0303"

function drawImage(src) {
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    var imageObj = new Image();

    imageObj.onload = function() {
    canvas.width = this.width;
    canvas.height = this.height;
    context.drawImage(imageObj, 0, 0, this.width,this.height);
    };
    imageObj.src = src
}

function drawBBoxes(blocks) {
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    
    blocks.forEach(bboxes => {
        bboxes.forEach(bbox => {
            context.lineWidth = 2
            debugger
            context.strokeStyle = bbox[4];
            drawLine(context, bbox[0], bbox[1]);
            drawLine(context, bbox[1], bbox[2]);
            drawLine(context, bbox[2], bbox[3]);
            drawLine(context, bbox[3], bbox[0]);
            // context.strokeRect(bbox[0], bbox[1], bbox[2], bbox[3]);
        });
    });
}

function drawLine(ctx, startPoint, endPoint) {
    ctx.beginPath();
    ctx.moveTo(startPoint[0], startPoint[1]);
    ctx.lineTo(endPoint[0], endPoint[1]);
    ctx.stroke();
}

function refreshBlocks(blocks) {
    blocks.forEach(bboxes => {
        bboxes.forEach(bbox => {
            bbox[4] = defaultcolor;
        });
    });
    return blocks
}

function highLighBlock(blocks, index) {
    blocks = refreshBlocks(blocks);
    
    blocks[index].forEach(bbox => {
        bbox[4] = highlightColor;
    });
    return blocks
}