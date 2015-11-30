__author__ = 'Den'

from os import listdir
from os.path import join, isfile
from math import log, e

spam_trashhold = 1.0 - 0.1 ** 15


class Classifier:
    def __init__(self, spmsges=[], hamsges=[], trashhold = 0.5):
        words_in_spam = {}
        for msg in spmsges:
            for word in msg:
                if word in words_in_spam:
                    words_in_spam[word] += 1
                else:
                    words_in_spam[word] = 1
        words_in_ham = {}
        for msg in hamsges:
            for word in msg:
                if word in words_in_ham:
                    words_in_ham[word] += 1
                else:
                    words_in_ham[word] = 1

        s = sum([len(msg) for msg in spmsges])
        h = sum([len(msg) for msg in hamsges])

        self.__log_spam_prob = {word: log(h * words_in_spam[word] / (h * words_in_spam[word] + s * words_in_ham.get(word, 1))) for word in words_in_spam}
        self.__log_ham_prob = {word: log(s * words_in_ham.get(word, 1) / (h * words_in_spam[word] + s * words_in_ham.get(word, 1))) for word in words_in_spam}
        self.__lower_bound = -log(s)
        self.__logarithmic_trashhold = log(1/trashhold - 1)
        # actually if we'll use trashhold = - 43 * log(10) then there will be no ham messages that are classified as spam

    def get_probabilities(self, msg):
        print(sum([self.__log_ham_prob.get(word, self.__lower_bound) - self.__log_spam_prob.get(word, self.__lower_bound) for word in msg]))
        probs = [e ** self.__log_spam_prob.get(word, self.__lower_bound) for word in msg]
        probs.sort()
        for prob in probs:
            print(prob, end=' ')
        print()

    def classify(self, msg):
        return sum([self.__log_ham_prob.get(word, self.__lower_bound) - self.__log_spam_prob.get(word, self.__lower_bound) for word in msg]) <= self.__logarithmic_trashhold

        # prob_spam, prob_ham = 1., 1.
        # for word in msg:
        #     prob_spam *= self.__log_spam_prob.get(word, self.__lower_bound)
        #     prob_ham *= 1 - self.__log_spam_prob.get(word, self.__lower_bound)
        # if prob_spam == 0.:
        #     return 0
        # return prob_spam / (prob_spam + prob_ham)


spmsges = [[] for i in range(10)]
hamsges = [[] for i in range(10)]


for i in range(10):
    for f in listdir('bayes/pu1/part' + str(i + 1)):
        cur = open(join('bayes/pu1/part' + str(i + 1), f))
        msg = {int(s) for s in cur.readline().split()[1:] + cur.readlines()[1].split()}
        if "spmsg" in f:
            spmsges[i].append(msg)
        else:
            hamsges[i].append(msg)


fp, tp, fn, tn = 0, 0, 0, 0
for i in range(10):  # i is number of part that is a testing set
    print("part", i, "is a testing set")
    classifier = Classifier([msg for j in range(10) for msg in spmsges[j] if j != i],
                            [msg for j in range(10) for msg in hamsges[j] if j != i],
                            spam_trashhold)

    for msg in spmsges[i]:
        if classifier.classify(msg):
            tp += 1
        else:
            fn += 1
    for msg in hamsges[i]:
        if classifier.classify(msg):
            fp += 1
            #classifier.get_probabilities(msg)
        else:
            tn += 1
print("___|___t___f")
print("  p|" + str(tp).ljust(4) + str(fp).ljust(4))
print("  n|" + str(tn).ljust(4) + str(fn).ljust(4))
print()

precision = tp / (tp + fp)
recall = tp / (tp + fn)
print("precision =", precision)
print("recall =", recall)
print("accuracy =", (tp + tn) / (tp + tn + fp + fn))
print("f1-measure =", 2 * precision * recall / (precision + recall))
