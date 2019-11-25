import os
import urllib.request
from flask import Flask, render_template, jsonify, request, flash, redirect, session
from werkzeug.utils import secure_filename
from utility import Utility
import cv2
import base64
from config import app

utility = Utility()

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/upload-image", methods=['POST'])
def upload():
    print('uploading')
    
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            flash('Không tìm thấy file')
            print('No file part')

        file = request.files['file']
        print('file: {}'.format(file))
        print('filename: {}'.format(file.filename))

        if file.filename == '':
            flash('Không tìm thấy file')
            print('No filename')

        if file and allowed_file(file.filename):
            img_name = secure_filename(file.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
            file.save(img_path)
            strings, bboxes = utility.recognize(img_path)
            
            img = utility.draw_box_on_image(bboxes, img_path)
            _, buffer_img= cv2.imencode('.jpg', img)
            data = base64.b64encode(buffer_img)
            
            session['bboxes'] = bboxes
            session['strings'] = strings
            session['img_path'] = img_path

            return {'status': 1, 'image': data.decode('utf-8'), 'strings': strings}
    
    return {'status': 0, 'image': None, 'strings': None}
    
@app.route("/upload-url", methods=['POST'])
def upload_url():
    print("upload url request")
    url = request.form["url"]
    print("url: {}".format(url))
    if url:
        img_path = utility.getFile(url)
        if img_path is None:
            return {'status': 0, 'image': None, 'strings': None}
            
        strings, bboxes = utility.recognize(img_path)

        img = utility.draw_box_on_image(bboxes, img_path)
        _, buffer_img= cv2.imencode('.jpg', img)
        data = base64.b64encode(buffer_img)

        session['bboxes'] = bboxes
        session['strings'] = strings
        session['img_path'] = img_path

        return {'status': 1, 'image': data.decode('utf-8'), 'strings': strings}
    
    return {'status': 0, 'image': None, 'strings': None}

@app.route("/mouse-hover", methods=["POST"])
def mouse_hover():
    content = request.form["content"]
    isHighLight = request.form["isHighLight"]
    print('isHighLight: {}'.format(isHighLight))

    strings = session['strings']
    bboxes = session['bboxes']
    img_path = session['img_path']

    index = strings.index(content)
    # bboxes = list(map(lambda block: [block[0], app.config['COLOR']], bboxes))
    color = app.config['HIGHLIGHT-COLOR'] if isHighLight == "true" else app.config['COLOR']
    print('color: {}'.format(color))
    bboxes[index][1] = color
    
    img = utility.draw_box_on_image(bboxes, img_path)
    _, buffer_img= cv2.imencode('.jpg', img)
    data = base64.b64encode(buffer_img)

    return {'image': data.decode('utf-8')}

if __name__ == "__main__":
    app.run(debug=True)
