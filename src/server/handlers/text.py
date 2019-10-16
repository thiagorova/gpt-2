from commons.text_model_singleton import TextGeneratorSingleton as tgs
from .base_handler import BaseHandler
from commons.errors import MISSING_FIELD
from tornado import escape
import base64
from .base_handler import BaseHandler

class TextHandler(BaseHandler):
    async def post(self):
        """
          get text based on input
        """
        data = escape.json_decode(self.request.body)
        if not data["text"]:
            self.write_error(MISSING_FIELD("text"))
        else:
          response = {}
          try:
            response["text"] = tgs.genSample(data["text"])
          except:
            tgs.clean()
            response["text"] = tgs.genSample(data["text"])
          self.write(response)

