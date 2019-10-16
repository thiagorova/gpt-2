from commons.get_text import TextGenerator

class TextGeneratorSingleton():
  @staticmethod
  def init_model():
    TextGeneratorSingleton.tg = TextGenerator()

  @staticmethod
  def clean():
    del TextGeneratorSingleton.tg
    TextGeneratorSingleton.init_model()

  @staticmethod
  def genSample(sample):
    try:
      return TextGeneratorSingleton.tg.get_sample(sample)
    except:
      TextGeneratorSingleton.init_model()
      return TextGeneratorSingleton.tg.get_sample(sample)


