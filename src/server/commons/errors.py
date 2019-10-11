"""
Create errors and stores API known errors
"""

class Error():
    """
    Handles all information we need to create an error
    """
    def __init__(self, error_name: str, error_message: str, http_status_code: int):
        self.error_message = error_message
        self.error_code = error_name
        self.http_status_code = http_status_code

    @property
    def json(self):
        """
        Creates an error json to be returned by our API
        """
        error_json = {
            "error_code" : self.error_code,
            "error_message" : self.error_message
        }
        return error_json

MALFORMED_JSON = Error("MALFORMED_JSON",
                       "The JSON could not be understood by the server due to malformed syntax.",
                       400)

RESOURCE_NOT_FOUND = Error("RESOURCE_NOT_FOUND", 'The requested resource was not found.', 404)

USER_DOES_NOT_EXIST = Error("USER_DOES_NOT_EXIST", 'The requested resource was not found.', 401)

METHOD_NOT_ALLOWED = Error("METHOD_NOT_ALLOWED",
                           "This method is not allowed. Please check API docs.", 405)

#We define 'field' as a key of a JSON passed in request's body
MISSING_FIELD = lambda key: Error("MISSING_FIELD",
                                  "Field {} is missing or has a null value.".format(key), 400)

#We define 'paramether' as a value in request's URL
MISSING_PARAMETER = lambda key: Error("MISSING_PARAMETER",
                                      "Paramether '{}' is missing or has a null value.".format(key), 400)

INVALID_FIELD = lambda key: Error("INVALID_FIELD",
                                  "Field '{}' is invalid for this request.".format(key), 400)

INVALID_PARAMETER = lambda key: Error("INVALID_PARAMETER",
                                      "Paramether '{}' is invalid for this request.".format(key), 400)

DATABASE_ERROR = Error("DATABASE_ERROR",
                       "Something went wrong in our database. Please report this error.", 500)

UNKWNOWN_ERROR = Error("UNKWNOWN_ERROR",
                       "Something went wrong. Please report this error.", 500)
