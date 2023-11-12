
class ErrorCake(Exception):
    status = None

    def __init__(self, message=None):
        self.message = message


class NotFoundCake(ErrorCake):
    status = 404


class InvalideCake(ErrorCake):
    status = 400
