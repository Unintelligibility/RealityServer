import numpy as np
import tensorflow as tf

hello = tf.constant('Hello')
sess = tf.Session()
print(sess.run(hello))
