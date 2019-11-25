import requests
import json
import cv2
from multiprocessing import Lock
import threading
import numpy as np
from config import app
import urllib
import mimetypes
import random
import string
import os

class Utility:
    def __init__(self):
        pass

    def draw_box_on_image(self, blocks, image_path):
        img = cv2.imread(image_path)
        for block in blocks:
            bboxes = block[0]
            color = block[1]
            for bbox in bboxes:
                cv2.line(img, (int(bbox[0][0]),int(bbox[0][1])), (int(bbox[1][0]),int(bbox[1][1])), color,2)
                cv2.line(img, (int(bbox[2][0]),int(bbox[2][1])), (int(bbox[1][0]),int(bbox[1][1])), color,2)
                cv2.line(img, (int(bbox[2][0]),int(bbox[2][1])), (int(bbox[3][0]),int(bbox[3][1])), color,2)
                cv2.line(img, (int(bbox[0][0]),int(bbox[0][1])), (int(bbox[3][0]),int(bbox[3][1])), color,2)
        
        return img

    def random_name(self, size=12, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def is_url_image(self, url):
        mimetype, _ = mimetypes.guess_type(url)
        return (mimetype and mimetype.startswith('image'))

    def check_url(self, url):
        try:
            headers={
            "Range": "bytes=0-10",
            "User-Agent": "Mozilla/5.0",
            "Accept": "*/*"
            }
            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req)
            return response.code in range(200,209)
        except Exception:
            return False

    def is_image_and_ready(self, url):
        mimetype = self.is_url_image(url)
        checkurl = self.check_url(url)
        print("Mimetype : {0}".format(mimetype))
        print("Check url : {0}".format(checkurl))
        return mimetype and checkurl

    def getFile(self, url):
        if self.is_image_and_ready(url):
            img_name = self.random_name() + ".jpg"
            print("Creating {0}".format(img_name))
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
            print("Image path for downloading ... {0}".format(image_path))
            urllib.request.urlretrieve(url, image_path)
            print("Finished download image")
            return image_path
        else:
            return None


    def recognize(self, img_path):
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'cache-control': 'no-cache',
            'Content-Type': 'image/png',
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
        }

        response = requests.post(app.config['API'], files={'file': (img_path, open(img_path, 'rb'), 'image/png', headers)})
        response_dict = json.loads(response.text)

        data = response_dict['data']

        strings = data['strings']
        bboxes = data['bboxes']

        bboxes = list(map(lambda bbox: [bbox, app.config['COLOR']], bboxes))
        # Struct of bboxes: [block, color], block = [bboxes], bboxes = [4 points]

        return (strings, bboxes)