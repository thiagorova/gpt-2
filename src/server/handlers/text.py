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
        try:
            response["text"] = tgs.genSample(data["text"], length)
        except:
            tgs.clean()
            response["text"] = tgs.genSample(data["text"], length)
        self.write(response)
