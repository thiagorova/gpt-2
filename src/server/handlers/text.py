from commons.text_model_singleton import TextGeneratorSingleton as tgs
from .base_handler import BaseHandler
from commons.errors import MISSING_FIELD
from commons.result_file import ResultFile
from tornado import escape
from tornado import gen
from tornado.web import asynchronous
from multiprocessing.pool import ThreadPool
from tornado.ioloop import IOLoop
from tornado.gen import coroutine
import base64
from .base_handler import BaseHandler
import multiprocessing, logging

mpl = multiprocessing.log_to_stderr()
mpl.setLevel(logging.INFO)
_workers = ThreadPool(10)

def run_background(func, callback, args=(), kwds={}):
    def _callback(result):
        IOLoop.instance().add_callback(lambda: callback(result))
    _workers.apply_async(func, args, kwds, _callback)

class TextHandler(BaseHandler):
    def get(self, id: str=None):
        response = {}
        if id is None:
            self.write_error(MISSING_FIELD("file id"))
        elif ResultFile.is_file_done(id) == False:
            response["done"] = False
            self.write(response)
        else:
            response["done"] = True
            response["text"] = ResultFile.get_file(id)
            ResultFile.erase_file(id)
            self.write(response)

    @asynchronous
    async def post(self):
        """
          get text based on input
        """
        data = escape.json_decode(self.request.body)
        try:
            length = int(data["length"])
        except:
            length = None

        try:
            data["text"]
        except:
            self.write_error(MISSING_FIELD("text"))
            return

        response = {}
        result_file = ResultFile.create_file()
        tgs.gen_sample(data["text"], length, result_file)
        #genSample(tgs.gen_sample, data["text"], length, result_file)
        response["text_id"] = result_file
        self.write(response)

@coroutine
def genSample(method, text, length, file_id):
    yield method(text, length, file_id)