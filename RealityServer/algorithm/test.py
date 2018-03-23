import numpy as np
import codecs
import jieba
import tensorflow as tf
import pymongo
from instance import my_mongo_config
from random import randint


def _getTrainBatch():
    the_labels = []
    arr = np.zeros([batchSize, max_seq])
    for t in range(batchSize):
        if t % 2 == 0:
            num = randint(1, int(len(title_neg) * 0.8))
            the_labels.append([1, 0])
        else:
            num = randint(int(len(title_neg) * 1.2), len(title_neg) + len(title_postive))
            the_labels.append([0, 1])
        arr[t] = ids[num - 1:num]
    return arr, the_labels


def _getTestBatch():
    the_labels = []
    arr = np.zeros([batchSize, max_seq])
    for t in range(batchSize):
        num = randint(int(len(title_neg) * 0.8), int(len(title_neg) * 1.2))
        if num <= len(title_neg):
            the_labels.append([1, 0])
        else:
            the_labels.append([0, 1])
        arr[t] = ids[num - 1:num]
    return arr, the_labels


# read the word vector from the pre-trained corpus
f = codecs.open('../corpus/zhwiki_2017_03.sg_50d.word2vec', 'r', 'utf-8')
wiki_words = []
line_ls = []
next(f)
for line in f:
    line_list = line.strip().split(' ')
    wiki_words.append(line_list[0])
    line_ls.append(np.array(line_list[1:]))
f.close()
wiki_words_vector = np.array(line_ls)

# read the negative title from txt
title_neg = []
f2 = codecs.open('../uc_title.txt', 'r', 'utf-8')
for line in f2:
    line = line.strip()
    title_neg.append(line)

# read the positive title from db
client = pymongo.MongoClient(my_mongo_config.MONGO_HOST,
                             username=my_mongo_config.MONGO_USERNAME,
                             password=my_mongo_config.MONGO_PASSWORD,
                             authSource=my_mongo_config.MONGO_AUTH_SOURCE,
                             authMechanism='SCRAM-SHA-1')
db = client.reality
cursor = db.news.find()
title_postive = []
for news in cursor:
    the_title = news['title']
    if '“假新闻”' in the_title:
        the_title = the_title[the_title.index('“假新闻”'):]
    if '(' in the_title:
        the_title = the_title[:the_title.index('(')]
    title_postive.append(the_title)

max_seq = 40
num_demension = 50

# example of the sentence to vector
sentence = '杨毅: 今天火箭败了! 火箭队: 脸疼不?'
sentence_np = np.zeros(max_seq, dtype='int32')
seg = jieba.cut(sentence)
for i in range(max_seq):
    if seg[i] in wiki_words:
        sentence_np[i] = wiki_words.index(seg[i])
    else:
        sentence_np[i] = wiki_words.index('Unknown')

ids = np.zeros((len(title_neg) + len(title_postive), max_seq), dtype='int32')

for x, title_n in enumerate(title_neg):
    for y, word in enumerate(jieba.cut(title_n)):
        if word in wiki_words:
            ids[x][y] = wiki_words.index(word)
        else:
            ids[x][y] = wiki_words.index('Unknown')
        if y >= max_seq:
            break

for x, title_n in enumerate(title_postive):
    for y, word in enumerate(jieba.cut(title_n)):
        if word in wiki_words:
            ids[x + len(title_neg)][y] = wiki_words.index(word)
        else:
            ids[x + len(title_neg)][y] = wiki_words.index('Unknown')
        if y >= max_seq:
            break

batchSize = 24
lstmUnits = 64
numClasses = 2
iterations = 100000
tf.reset_default_graph()

labels = tf.placeholder(tf.float32, [batchSize, numClasses])
input_data = tf.placeholder(tf.int32, [batchSize, max_seq])

data = tf.Variable(tf.zeros([batchSize, max_seq, num_demension]), dtype=tf.float32)

lstmCell = tf.contrib.rnn.BasicLSTMCell(lstmUnits)
lstmCell = tf.contrib.rnn.DropoutWrapper(cell=lstmCell, output_keep_prob=0.75)
value, _ = tf.nn.dynamic_rnn(lstmCell, data, dtype=tf.float32)

weight = tf.Variable(tf.truncated_normal([lstmUnits, numClasses]))
bias = tf.Variable(tf.constant(0.1, shape=[numClasses]))
value = tf.transpose(value, [1, 0, 2])
last = tf.gather(value, int(value.get_shape()[0]) - 1)
prediction = (tf.matmul(last, weight) + bias)

correctPred = tf.equal(tf.argmax(prediction, 1), tf.argmax(labels, 1))
accuracy = tf.reduce_mean(tf.cast(correctPred, tf.float32))

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=labels))
optimizer = tf.train.AdamOptimizer().minimize(loss)

sess = tf.Session()
sess.run(tf.global_variables_initializer())

saver = tf.train.Saver()
for i in range(iterations):
    # Next Batch of reviews
    nextBatch, nextBatchLabels = _getTrainBatch()
    sess.run(optimizer, {input_data: nextBatch, labels: nextBatchLabels})

    # Save the network every 10,000 training iterations
    if i % 10000 == 0 and i != 0:
        save_path = saver.save(sess, "models/pretrained_lstm.ckpt", global_step=i)
        print("saved to %s" % save_path)
