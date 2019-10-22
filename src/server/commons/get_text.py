#!/usr/bin/env python
# coding: utf8

import json
import os
import re
import numpy as np
import tensorflow as tf
import commons.model as model
import commons.sample as sample
import commons.encoder as encoder
from commons.result_file import ResultFile

class TextGenerator():
    def __init__(
        self,
        model_name='124M',
        seed=None,
        nsamples=1,
        batch_size=1,
        temperature=1,
        length=None,
        top_k=40,
        top_p=1,
        models_dir='models',
    ):
        models_dir = os.path.expanduser(os.path.expandvars(models_dir))
        if batch_size is None:
            batch_size = 1
        assert nsamples % batch_size == 0
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p
        self.model_name = model_name
        self.models_dir = models_dir
        self.enc = encoder.get_encoder(model_name, models_dir)
        self.hparams = model.default_hparams()
        with open(os.path.join(models_dir, model_name, 'hparams.json')) as f:
            self.hparams.override_from_dict(json.load(f))

        self.batch_size = batch_size
        self.sess = tf.compat.v1.Session()
        self.context = tf.placeholder(tf.int32, [batch_size, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)

        self.setTrainer(length, top_k)

    def __del__(self):
        try:
            self.sess.close()
        except:
            pass

    def get_sample(self, sample_text, result_file, length=None, top_k=None):
        """
          gets trained model and applies it to user sample
        """
        #self.setTrainer(length, top_k)
        context_tokens = self.enc.encode(sample_text)
        print('generating text')
        out = self.sess.run(self.output, feed_dict={
            self.context: [context_tokens for _ in range(self.batch_size)]
        })[:, len(context_tokens):]
        print('text generated')
        text = self.enc.decode(out[0])
        text = self.limit_text(text, length)
        ResultFile.write_to_file(result_file, text)

    def limit_text (self, text, length):
        if length is None or length >= len(text):
            return text
        pos = length
        reTerm = re.compile(u'[.,;()[\]!?"―“”–:•«€¨⁄•±‚ ©ªº@∫~∞‘¡“¶¢|≠¿´`]', re.UNICODE)
        while re.search(reTerm, text[pos]) and pos > 0:
            pos -= 1
        if pos < 2:
            return text
        return text[:pos]


    def setTrainer (self, length, top_k):
        if top_k is None:
            top_k = self.top_k
        if length is None:
            length = self.hparams.n_ctx // 2
        elif length > self.hparams.n_ctx:
            raise ValueError(
                "Can't get samples longer than window size: %s" % self.hparams.n_ctx)
        self.output = sample.sample_sequence(
            hparams=self.hparams, length=length,
            context=self.context,
            batch_size=self.batch_size,
            temperature=self.temperature, top_k=top_k, top_p=self.top_p
        )

        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(self.models_dir, self.model_name))
        saver.restore(self.sess, ckpt)