class Response_msg(object):
    def __init__(self):
        self.data=None
        self.code=1000
        self.error=None
    @property
    def dict(self):
        return self.__dict__