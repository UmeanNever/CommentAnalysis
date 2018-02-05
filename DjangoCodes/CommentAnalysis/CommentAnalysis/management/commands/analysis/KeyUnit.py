# -*- coding: utf-8 -*-

class keydata(object):
    def __init__(self, ID, keyword, weight, sentence, sentiment, textID, date):
        self.ID = ID
        self.keyword = keyword
        self.weight = weight
        self.sentence = [[sentence, date]]
        self.sentiment = sentiment
        self.textID = [textID]
        self.num = 1
        self.adjs = {}
        self.date = date

    def tran_to_dict(self):
        dict = {'name': self.keyword, 'sentiment': self.sentiment}
        if self.adjs:
            dict['expressions'] = self.adjs
        dict['sentence'] = self.sentence
        return dict
