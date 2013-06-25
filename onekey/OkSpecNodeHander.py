import time

class OkSpecNodeHandler(object):
    @classmethod
    def callback(cls,  name,  *args):
        method = getattr(cls,  name,  None)
        if callable(method):
            return method(*args)
        return None
    
    def
    
    @classmethod
    def methodList(cls):
        return {"testunit_wait": {"id": "wait", "type": "minute"}}
