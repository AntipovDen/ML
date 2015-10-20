__author__ = 'Den'

from os import listdir
from os.path import join, isfile

spam_border = 0.8

words_in_spam = {}
words_in_ham = {}
spmsg_count = 0
hamsg_count = 0


# TODO: we should go through all the files from the learning set
for f in listdir('bayes/pu1/part1'):
    cur = open(join('bayes/pu1/part1', f))
    is_spam = "spmsg" in f
    words = {int(i) for i in cur.readline().split()[1:]}
    for i in cur.readlines()[1].split(' '):
        words.add(int(i))
    for word in words:
        if is_spam:
            spmsg_count += 1
            if word in words_in_spam:
                words_in_spam[word] += 1
            else:
                words_in_spam[word] = 1
        else:
            hamsg_count += 1
            if word in words_in_ham:
                words_in_ham[word] += 1
            else:
                words_in_ham[word] = 1


word_spaming = {word: words_in_spam[word] / spmsg_count for word in words_in_spam}
word_haming = {word: words_in_ham[word] / hamsg_count for word in words_in_ham}
for word in word_spaming:
    if word not in word_haming:
        word_haming[word] = 0

# probability that message is spam if it contains a word
spam_prob = {word_spaming[word] / (word_spaming[word] + word_haming[word]) for word in word_spaming}

def msg_spam_prob(msg):
    prob_spam, prob_ham = 1., 1.
    for word in msg:
        prob_spam *= spam_prob[word]
        prob_ham *= 1 - spam_prob[word]
    return prob_spam / (prob_spam + prob_ham)

# TODO: cross-validation should be here