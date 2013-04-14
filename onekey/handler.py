class handler(object):
    def callback(self,  name,  *args):
        method = getattr(self,  name,  None) 
        if callable(method):
            return method(*args)
            
