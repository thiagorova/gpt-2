"""
Authorship application based on Tornado Web Server
"""
import tornado.ioloop
import tornado.web
from time import time
from commons.rds_singleton import RDSSingleton
from datetime import datetime

class Application(tornado.web.Application):
    """
    Authorship application based on Tornado Web Server
    """
    def __init__(self, rds, handlers):
        settings = dict(debug=True)
        self.up_time = int(time())
        self.up_time_iso = datetime.now().isoformat(' ')
        self.request_counter = 0
        super(Application, self).__init__(handlers, **settings)
        #RDSSingleton(rds())
