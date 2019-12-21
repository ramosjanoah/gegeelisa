from http import HTTPStatus
from env import env

class GegeException(Exception):
    def __init__(self):
        self.message = "Error"
        self.http_code = 400
        self.private_code = 0
        if env['DEBUG_MODE']:
            self.serialize_func = self.__serialize_all
        else:
            self.serialize_func = self.__serialize_code_only

    def serialize(self):
        return self.serialize_func()

    def __serialize_all(self):
        return {
            "meta": {
                "http_status": self.http_code,
                "private_code": self.private_code,
                "message": self.message,
            }
        }
    
    def __serialize_code_only(self):
        return {
            "meta": {
                "http_status": self.http_code,
                "private_code": self.private_code,
            }
        }


class WrongException(GegeException):
    def __init__(self):
        super().__init__()
        self.message = "You're doing something wrong."
        self.http_code = HTTPStatus.BAD_REQUEST
        self.private_code = 4000

class ErrorException(GegeException):
    def __init__(self):
        super().__init__()
        self.message = "There's error on the app."
        self.http_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.private_code = 5000

class PageSavedButNotChecked(WrongException):
    def __init__(self):
        super().__init__()
        self.message = "The page wanted to be scrapped, but not checked on database first."
        self.http_code = HTTPStatus.FORBIDDEN
        self.http_code = 4031

class PageHasBeenScrapped(WrongException):
    def __init__(self):
        super().__init__()
        self.message = "The page has been scrapped."
        self.http_code = HTTPStatus.FORBIDDEN
        self.http_code = 4032

class PageHasBeenFounded(WrongException):
    def __init__(self):
        super().__init__()
        self.message = "The page has been founded."
        self.http_code = HTTPStatus.FORBIDDEN
        self.http_code = 4033


class NodeNotFound(WrongException):
    def __init__(self):
        super().__init__()
        self.message = "Node is not found."
        self.http_code = HTTPStatus.NOT_FOUND
        self.private_code = 4041

class PageNotFound(WrongException):
    def __init__(self):
        super().__init__()
        self.message = "Page not found."
        self.http_code = HTTPStatus.NOT_FOUND
        self.private_code = 4042

class BadRequest(WrongException):
    def __init__(self, message, private_code=0):
        super().__init__()
        self.message = 'Bad Request: {}'.format(message)
        self.http_code = 400
        self.private_code = private_code
        self.private_code = 4001

class InvalidParameter(WrongException):
    def __init__(self, param):
        super().__init__()
        self.message = "Invalid parameter: '{}'".format(param)
        self.http_code = 400
        self.private_code = 4002

class InvalidType(WrongException):
    def __init__(self, var_name, correct_type):
        super().__init__()
        self.message = "Invalid type. {} should have type {}".format(var_name, str(correct_type))
        self.http_code = 422
        self.private_code = 4221

class NodeHasBeenBuild(WrongException):
    def __init__(self):
        super().__init__()
        self.message = "The node has been build"
        self.http_code = 403
        self.private_code = 4033

class PageHasNotBeenSet():
    def __init__(self):
        super().__init__()
        self.message = "The node has not been saved but want to be saved."
        self.http_code = 403
        self.private_code = 4033


class ScrapePageError(GegeException):
    def __init__(self):
        super().__init__()
        self.message = "The page currently cannot be scrapped"
        self.http_code = 422
        self.private_code = 4222

class PageHasBeenExpanded(GegeException):
    def __init__(self):
        super().__init__()
        self.message = "The node has been expanded"
        self.http_code = 403
        self.private_code = 4033
