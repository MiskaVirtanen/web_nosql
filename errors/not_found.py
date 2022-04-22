class NotFound(Exception):
    def __init__(self, message='Not found'):
        self.args = (message,)