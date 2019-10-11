import time

from calendar import timegm
from tornado.gen import coroutine
from tornado.web import RequestHandler
from tornado.escape import json_decode
from json.decoder import JSONDecodeError
from commons.errors import Error, MALFORMED_JSON, INVALID_FIELD, MISSING_FIELD

class BaseHandler(RequestHandler):
    """
    Base Handler class to be extended by all handlers
    """
    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')
        self.set_header("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, \
                         Origin,Accept, X-Requested-With, Content-Type, \
                         Access-Control-Request-Method, Access-Control-Request-Headers")

    async def options(self, argA=None, argB=None):
        self.set_status(204)
        self.finish()

    def write_error(self, error: Error):
        self.set_status(error.http_status_code)
        self.finish(error.json)

    def get_data(self, req_keys: list = None, acc_keys: list = None) -> dict:
        """
        Gets data from request's body and validate if json's keys are valid or not
        """
        try:
            data = json_decode(self.request.body)
            if req_keys:
                for i in req_keys:
                    if i not in data:
                        raise KeyError(i)
            if acc_keys:
                for i in data:
                    if i not in acc_keys:
                        raise ValueError(i)
        except JSONDecodeError:
            self.write_error(MALFORMED_JSON)
            return {}
        except KeyError as k:
            self.write_error(MISSING_FIELD(k))
            return {}
        except ValueError as k:
            self.write_error(INVALID_FIELD(k))
            return {}
        return data

    def date_to_seconds(self, date: int):
        mytimestamp = time.strptime(date, "%Y-%m-%e-%H:%M:%S")
        return timegm(mytimestamp)

#Isso é apenas uma demonstração sobre como usar corrotinas e decorators no Tornado
def request_counter(method):
    """
    This anotation specify whether the request should be counted or not
    """
    @coroutine
    def counter(*args, **kw):
        """Adds +1 to application request counter"""
        handler = args[0]
        handler.application.request_counter += 1
        yield method(*args, **kw)
    return counter
