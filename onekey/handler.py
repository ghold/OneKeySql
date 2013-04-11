class handler(object):
    def callback(self,  name,  *args):
        method = "call_" + name
        if self.callable(method):
            return method(*args)
            
