import requests
import json
import cv2
from multiprocessing import Lock
import threading
import numpy as np
# lock = threadhing.lock

# def synchronized(lock):
#     """ Synchronization decorator """
#     def wrapper(f):
#         @functools.wraps(f)
#         def inner_wrapper(*args, **kw):
#             with lock:
#                 return f(*args, **kw)
#         return inner_wrapper
#     return wrapper

# def singleton(theClass):
#     """ decorator for a class to make a singleton out of it """
#     classInstances = {}
#     synchronized(lock)
#     def getInstance(*args, **kwargs):
#         """ creating or just return the one and only class instance.
#             The singleton depends on the parameters used in _init_ """
#         key = (theClass, args, str(kwargs))
#         if key not in classInstances:
#             classInstances[key] = theClass(*args, **kwargs)
#         return classInstances[key]

#     return getInstance

# @singleton
class Utility:

    service_url="http://172.26.6.30:8000/adtechhcm/text_recognize_image?"

    def __init__(self):
        pass


    def draw_box_on_image(self, bboxes, image_path):
        img = cv2.imread(image_path)
        for bbox in bboxes:
            cv2.line(img, (int(bbox[0][0]),int(bbox[0][1])), (int(bbox[1][0]),int(bbox[1][1])), (0,255,0),2)
            cv2.line(img, (int(bbox[2][0]),int(bbox[2][1])), (int(bbox[1][0]),int(bbox[1][1])), (0,255,0),2)
            cv2.line(img, (int(bbox[2][0]),int(bbox[2][1])), (int(bbox[3][0]),int(bbox[3][1])), (0,255,0),2)
            cv2.line(img, (int(bbox[0][0]),int(bbox[0][1])), (int(bbox[3][0]),int(bbox[3][1])), (0,255,0),2)
        
        return img

    def recognize(self, img_path):
        url = 'http://192.168.20.166:8080/text_recognize'
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'cache-control': 'no-cache',
            'Content-Type': 'image/png',
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
        }

        response = requests.post(url, files={'file': (img_path, open(img_path, 'rb'), 'image/png', headers)})
        response_dict = json.loads(response.text)

        blocks = response_dict['data']['blocks']
        bboxes = response_dict['data']['bboxes']

        return (blocks, bboxes)