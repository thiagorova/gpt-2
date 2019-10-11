from commons.get_text import TextGenerator
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
          response["text"] = TextGenerator.get_sample(data["text"])
          self.write(response)

