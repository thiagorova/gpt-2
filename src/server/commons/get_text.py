import json
import os
import numpy as np
import tensorflow as tf
import commons.model as model
import commons.sample as sample
import commons.encoder as encoder

class TextGenerator():
  def __init__(
    self,
    model_name='774M',
    seed=None,
    nsamples=1,
    batch_size=1,
    length=None,
    temperature=1,
    top_k=40,
    top_p=1,
    models_dir='models',
  ):
    models_dir = os.path.expanduser(os.path.expandvars(models_dir))
    if batch_size is None:
      batch_size = 1
    assert nsamples % batch_size == 0

    self.enc = encoder.get_encoder(model_name, models_dir)
    hparams = model.default_hparams()
    with open(os.path.join(models_dir, model_name, 'hparams.json')) as f:
      hparams.override_from_dict(json.load(f))

    if length is None:
      length = hparams.n_ctx // 2
    elif length > hparams.n_ctx:
      raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)
    self.batch_size = batch_size
    self.sess = tf.compat.v1.Session()
    self.context = tf.placeholder(tf.int32, [batch_size, None])
    np.random.seed(seed)
    tf.set_random_seed(seed)
    self.output = sample.sample_sequence(
      hparams=hparams, length=length,
      context=self.context,
      batch_size=batch_size,
      temperature=temperature, top_k=top_k, top_p=top_p
    )

    saver = tf.train.Saver()
    ckpt = tf.train.latest_checkpoint(os.path.join(models_dir, model_name))
    saver.restore(self.sess, ckpt)

  def __del__(self):
    self.sess.close()

  def get_sample(self, sample_text):
    """
      gets trained model and applies it to user sample
    """
    context_tokens = self.enc.encode(sample_text)
    out = self.sess.run(self.output, feed_dict={
      self.context: [context_tokens for _ in range(self.batch_size)]
    })[:, len(context_tokens):]
    return self.enc.decode(out[0])
