#!/usr/bin/python
#
#   FILE: naivebayes_testing.py
#   DATE: October , 2014
#   Author: Mudra Ladani
#
#   Simple example of building a user feedback classifier.
#
#   Copyright by Author. All rights reserved. Not for reuse without
#   express permissions.
#
import sys, csv, nltk
from infx.utils.stop_words import remove_stops, STOPLIST

# Stop word list
stopWords = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also',
             'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be',
             'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear',
             'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for',
             'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers',
             'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is',
             'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may',
             'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor',
             'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our',
             'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since',
             'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then',
             'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us',
             've', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which',
             'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet',
             'you', 'your']

#function to remove stopwords
def remove_stopwords(feedback):
    for i in stopWords:
      feedback.replace(i,"")
    return feedback


class Sentiment(object):
    def __init__(self):
        self.complete_token_list = []
        self.training_data = None
        self.classifier = None
    
    # Load a CSV file
    def load_csv_label_data(self,fname=""):
        label_data = []
        if( fname ):
            lines = 0
            junk = 0
            none_junk = 0
            unknown = 0
            f = open(fname,"rU")
            reader = csv.DictReader(f,dialect="excel")
            rec = reader.next()
            while rec:
                lines += 1
                user_text = rec['message1']
                clean_tweet = remove_stopwords(user_text)
                token_list = clean_tweet.split()
                token_list = clean_tweet.split()
                if( (rec['label']=="junk") ):
                    #tup = tuple(token_list,"positive")
                    tup = (token_list,"junk")
                    self.complete_token_list.extend(token_list)
                    junk += 1
                elif( (rec['label']=="none-junk") ):
                    #tup = tuple(token_list,"negative")
                    tup = (token_list,"none-junk")
                    self.complete_token_list.extend(token_list)
                    none_junk += 1
                else:
                    # this one is neutral or not labeled
                    unknown += 1
                label_data.append(tup)
                try:
                    rec = reader.next()
                except:
                    rec = None
            f.close()
        print label_data
        print lines
        print junk
        print none_junk
        print unknown
        return [label_data,lines,junk,none_junk,unknown]
    
    def load_csv_data(self,fname=""):
        test_data = []
        if( fname ):
            lines = 0
            f = open(fname,"rU")
            reader = csv.DictReader(f,dialect="excel")
            rec = reader.next()
            while rec:
                lines += 1
                user_text = rec['message1']
                test_data.append(user_text)
                try:
                    rec = reader.next()
                except:
                    rec = None
            f.close()
        print test_data
        print lines
        return [test_data,lines]

    def features(self, doc):
        feature_dict = {}
        for tok in self.complete_token_list:
            feature_dict[tok] = (tok in doc)
        return feature_dict
    
    
    def new_classifier(self, label_data=None):
        self.training_data = nltk.classify.apply_features(self.features,label_data)
        self.classifier = nltk.classify.naivebayes.NaiveBayesClassifier.train(self.training_data)
        #self.classifier = nltk.NaiveBayesClassifier.train(self.training_data)
        return 
    
    def top_n_features(self, n=10):
        self.classifier.show_most_informative_features(n=n)
    
    def score(self, text):
        return self.classifier.classify(self.features(text))


def score_tweets(sent=None,feedback_list=None):
    for feedback in feedback_list:
        score = sent.score(feedback)
        print "%s:"%score,feedback


s = Sentiment()
result = s.load_csv_label_data(fname="concurtest.csv")
s.new_classifier(label_data=result[0])
s.top_n_features(n=30)
new_data = s.load_csv_data(fname="concurtest2.csv")

print new_data
score_tweets(sent=s,feedback_list=new_data[0])
