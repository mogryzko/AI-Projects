'''
Original performance:
Precision:0.9508196721311475 Recall:0.8656716417910447 F-Score:0.9062499999999999 Accuracy:97.84560143626571

Tuned performance:
I was unable to get a better performance than my original by changing my c and k values
'''



import sys
import string
import math


def extract_words(text):
    translator = str.maketrans('', '', string.punctuation)
    extracted = text.translate(translator).lower()
    words = extracted.split()
    return words # should return a list of words in the data sample.


class NbClassifier(object):

    def __init__(self, training_filename, stopword_file = None):
        self.attribute_types = set()
        self.label_prior = {}    
        self.word_given_label = {}
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

    def train(self, training_filename):
        c = 1
        myfile = open(training_filename, 'r')
        data = myfile.readlines()
        countwy = {'spam': 0, 'ham': 0}
        self.label_prior = {'ham': 0, 'spam': 0}
        wglcount = {}
        for line in data:
            words = extract_words(line)
            mess = ''
            oppmess = ''
            if words[0] == 'ham':
                self.label_prior['ham'] += 1
                mess = 'ham'
                oppmess = 'spam'
            elif words[0] == 'spam':
                self.label_prior['spam'] += 1
                mess = 'spam'
                oppmess = 'ham'
            for word in words:
                if word != 'ham' and word != 'spam' and word in self.attribute_types:
                    countwy[mess] += 1
                    if (word,mess) in wglcount:
                        wglcount[(word, mess)] += 1
                    else:
                        wglcount[(word, mess)] = 1
                        if (word, oppmess) not in wglcount:
                            wglcount[(word, oppmess)] = 0
        for word in self.attribute_types:
            self.word_given_label[(word,'spam')] = (wglcount[(word,'spam')] + c)/(countwy['spam'] + c*len(self.attribute_types))
            self.word_given_label[(word,'ham')] = (wglcount[(word,'ham')] + c)/(countwy['ham'] + c*len(self.attribute_types))
        myfile.close()

    def predict(self, text):
        words = extract_words(text)
        words.pop(0)
        numspam = self.label_prior['spam']
        numham = self.label_prior['ham']
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
