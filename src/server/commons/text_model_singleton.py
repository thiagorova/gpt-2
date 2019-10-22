import string
from multiprocessing.pool import ThreadPool
from commons.get_text import TextGenerator
from random import choice

class TextGeneratorSingleton():
  @staticmethod
  def init_model():
    TextGeneratorSingleton.tg = TextGenerator()

  @staticmethod
  def clean():
    try:
      del TextGeneratorSingleton.tg
    except:
      pass
    TextGeneratorSingleton.init_model()

  @staticmethod
  def gen_sample(sample, length=None, result_file=None):
    try:
      TextGeneratorSingleton.tg
    except:
      TextGeneratorSingleton.clean()
    pool = ThreadPool()
    pool.apply_async(TextGeneratorSingleton.tg.get_sample, args=(sample, result_file, length))

