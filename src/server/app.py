"""
Authorship PROD application based on Tornado Web Server
"""
import sys
import tornado.ioloop
import tornado.web
from tornado.log import enable_pretty_logging
from commons.rds import RDS
from routes import ROUTES
from application import Application

if __name__ == "__main__":
    enable_pretty_logging()

    ARGS = sys.argv
    ARGS.append("--log_file_prefix=my_app.log")
    tornado.options.parse_command_line(ARGS)

    APP = Application(rds=RDS, handlers=ROUTES)
    APP.listen(8892, max_buffer_size=1000000000)
    tornado.ioloop.IOLoop.current().start()

