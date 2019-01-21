'''
Performance:
Precision:0.9491525423728814 Recall:0.8888888888888888 F-Score:0.9180327868852458 Accuracy:98.20466786355476

'''



import sys
import string
import math


c = 1 # smoothing constant

# returns a list of words in the data sample.
def extract_words(text):
    translator = str.maketrans('', '', string.punctuation)
    extracted = text.translate(translator).lower()
    words = extracted.split()
    return words


class NbClassifier(object):

    def __init__(self, training_filename, stopword_file = None):
        self.attribute_types = set()
        self.label_prior = {} # total number of words in all messages marked as spam or ham
        self.word_given_label = {} # final probability of word given label
        self.stopwords = ['a','an','and','are','as','at','be','been','by','for','from','has','have','in','is','it',
                          'its','of','on','that','the','to','was','were','will','with']


        self.collect_attribute_types(training_filename, 0)
        self.train(training_filename)

    def collect_attribute_types(self, training_filename, k):
        myfile = open(training_filename, 'r')
        data = myfile.read()
        words = extract_words(data)
        word_set = set(words)
        word_set.remove('ham')
        word_set.remove('spam')
        for word in word_set:
            wordfreq = words.count(word)
            if (wordfreq >= k) and word not in self.stopwords:
                self.attribute_types.add(word)
        myfile.close()

    # True means spam message, False means ham message
    def train(self, training_filename):
        myfile = open(training_filename, 'r')
        countwy = {True: 0, False: 0} # number of words in ham and spam messages
        self.label_prior = {True: 0, False: 0}
        wglcount = {} # number of times word is seen in spam/ham message
        for line in myfile:
            words = extract_words(line)
            tf = False
            if words[0] == 'ham':
                self.label_prior[False] += 1
                tf = False
            elif words[0] == 'spam':
                self.label_prior[True] += 1
                tf = True
            for i in range(1, len(words)):
                countwy[tf] += 1
                wglcount.setdefault((words[i],tf), 0)
                wglcount[(words[i], tf)] += 1
                if (words[i], not tf) not in wglcount:
                    wglcount[(words[i], not tf)] = 0
        for word in self.attribute_types:
            self.word_given_label[(word,'spam')] = (wglcount[(word,True)] + c)/(countwy[True] + c*len(self.attribute_types))
            self.word_given_label[(word,'ham')] = (wglcount[(word,False)] + c)/(countwy[False] + c*len(self.attribute_types))
        myfile.close()

    def predict(self, text):
        words = extract_words(text)
        words.pop(0)
        numspam = self.label_prior[True]
        numham = self.label_prior[False]
        probspam = math.log10(numspam)
        probham = math.log10(numham)
        for word in words:
            if word in self.attribute_types:
                probspam += math.log10(self.word_given_label[(word,'spam')])
                probham += math.log10(self.word_given_label[(word,'ham')])
        probdict = {'spam': probspam, 'ham': probham}
        return probdict


    def evaluate(self, test_filename):
        truepos = 0
        trueneg = 0
        falsepos = 0
        falseneg = 0

        with open(test_filename, 'r') as myfile:
            for line in myfile:
               dict = self.predict(line)
               list = extract_words(line)
               if dict['spam'] > dict['ham'] and list[0] == 'spam':
                   truepos += 1
               elif dict['spam'] > dict['ham'] and list[0] == 'ham':
                   falsepos += 1
               elif dict['spam'] < dict['ham'] and list[0] == 'ham':
                   trueneg += 1
               elif dict['spam'] < dict['ham'] and list[0] == 'spam':
                   falseneg += 1

        myfile.close()
        precision = truepos/(truepos + falsepos)
        recall = truepos/(truepos + falseneg)
        fscore = (2 * precision * recall)/(precision + recall)
        accuracy = 100*(trueneg + truepos)/(trueneg + truepos + falsepos + falseneg)
        return (precision, recall, fscore, accuracy)


def print_result(result):
    print("Precision:{} Recall:{} F-Score:{} Accuracy:{}".format(*result))


if __name__ == "__main__":
    
    classifier = NbClassifier(sys.argv[1])
    result = classifier.evaluate(sys.argv[2])
    print_result(result)
