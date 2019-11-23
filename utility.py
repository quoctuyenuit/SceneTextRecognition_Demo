import requests
import json
import cv2
from multiprocessing import Lock
import threading
import numpy as np
from config import app

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