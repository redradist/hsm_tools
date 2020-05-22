class ValidationError(Exception):
    def __init__(self, **kwargs):
        if 'msg' in kwargs:
            self._message = kwargs['msg']
