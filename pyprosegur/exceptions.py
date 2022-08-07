class ProsegurException(Exception):
    """Exception raised py pyprosegur."""

class BackendError(ProsegurException):
    """Error to indicate backend did not return something usefull."""

class NotFound(ProsegurException):
    """Error to indicate the request object was not found."""