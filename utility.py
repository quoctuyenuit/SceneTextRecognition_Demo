import requests

def synchronized(lock):
    """ Synchronization decorator """
    def wrapper(f):
        @functools.wraps(f)
        def inner_wrapper(*args, **kw):
            with lock:
                return f(*args, **kw)
        return inner_wrapper
    return wrapper

def singleton(theClass):
    """ decorator for a class to make a singleton out of it """
    classInstances = {}
    synchronized(lock)
    def getInstance(*args, **kwargs):
        """ creating or just return the one and only class instance.
            The singleton depends on the parameters used in _init_ """
        key = (theClass, args, str(kwargs))
        if key not in classInstances:
            classInstances[key] = theClass(*args, **kwargs)
        return classInstances[key]

    return getInstance

@singleton
class Utility:

    service_url="http://172.26.6.30:8000/adtechhcm/text_recognize_image?"

    def __init__(self):
        pass

    def recognize(self, image):
        headers = {'Content-type': "image/png"}
        files={'file': open(image, 'rb')}
        r = requests.post(url, files=files, headers=headers)
        return r.content


