from commons.get_text import TextGenerator

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
  def genSample(sample, length=None):
    try:
      return TextGeneratorSingleton.tg.get_sample(sample, length)
    except:
      TextGeneratorSingleton.init_model()
      return TextGeneratorSingleton.tg.get_sample(sample, length)


