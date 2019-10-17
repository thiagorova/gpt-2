"""
Authorship PROD application based on Tornado Web Server
"""
import sys
import tornado.ioloop
import tornado.web
from tornado.log import enable_pretty_logging
from routes import ROUTES
from commons.text_model_singleton import TextGeneratorSingleton as tgs

if __name__ == "__main__":
    enable_pretty_logging()
    print('Starting system setup')
    ARGS = sys.argv
    ARGS.append("--log_file_prefix=my_app.log")
    tornado.options.parse_command_line(ARGS)

    APP = tornado.web.Application(handlers=ROUTES)
    APP.listen(8892, max_buffer_size=1000000000)
    print('Starting model training')
    tgs.init_model()
    print('System ready to roll')
    tornado.ioloop.IOLoop.current().start()

