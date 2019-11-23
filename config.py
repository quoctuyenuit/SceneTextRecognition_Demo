from flask import Flask

UPLOAD_FOLDER = './static/images/uploads'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['API'] = 'http://192.168.20.166:8080/text_recognize'
app.config['COLOR'] = (0,255,0)
app.config['HIGHLIGHT-COLOR'] = (255,0,0)