#from handlers.users import UserHandler
from handlers.text import TextHandler

ROUTES = [
    (r"/text/?", TextHandler),
    #(r"/users/(.+?)/transcriptions/(.{,12})/?", TexttHandler),
]