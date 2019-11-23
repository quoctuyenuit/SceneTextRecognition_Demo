import os
import urllib.request
from flask import Flask, render_template, jsonify, request, flash, redirect, session
from werkzeug.utils import secure_filename
from utility import Utility
import cv2
import base64

app = Flask(__name__)
UPLOAD_FOLDER = './static/images/uploads'
DREW_FOLDER = './static/images/uploads/drew'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DREW_FOLDER'] = DREW_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['IMAGE']=''

utility = Utility()

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

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
            blocks, bboxes = utility.recognize(img_path)
            img = utility.draw_box_on_image(bboxes, img_path)

            drew_path = os.path.join(app.config['DREW_FOLDER'], img_name)
            cv2.imwrite(drew_path, img)
           
            return {'status': 1, 'image': drew_path, 'blocks': blocks}
    
    return {'status': 0, 'image': drew_path, 'blocks': blocks}
    
if __name__ == "__main__":
    app.run(debug=True)
