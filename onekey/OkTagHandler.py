class OkTagHandler(object):
    
    @classmethod
    def callback(cls,  name,  *args):
        method = getattr(cls,  name,  None)
        if callable(method):
            return method(*args)
    @classmethod        
    def datetime(cls, *args):
        from OkEdit import OkDatetimeEdit
        return OkDatetimeEdit()
    @classmethod    
    def text(cls, *args):
        from OkEdit import OkTextEdit
        return OkTextEdit()

