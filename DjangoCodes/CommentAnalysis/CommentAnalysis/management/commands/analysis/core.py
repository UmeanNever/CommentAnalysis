# -*- coding: utf-8 -*-
from __future__ import division
import KeyUnit
import re
from glob import glob
import codecs
import numpy as np
from snownlp import SnowNLP
import jieba.analyse as phrase_extract
import jieba.posseg as pseg
import jieba
import json
import gensim
import itertools


def parse_month(time):
    parsed_date = re.split('-| ', time)
    return "{0}{1}".format(str(parsed_date[0]), str(parsed_date[1]))


def compair(x):
    return x[1]


def locate(word, text, flag):
    mid = text.find(word)
    l = mid
    r = mid
    length = len(text)
    cstr = u'。！ ？；\n.?!; '
    if flag == 1:
        # print word, text
        lt, rt = text.split(word)
        return lt + u' <<' + word + u' >> ' + rt
    while cstr.find(text[l]) == -1:
        if text[l] == u'，' and mid - l > 10:
            break
        l -= 1
        if l < 0:
            break
    while cstr.find(text[r]) == -1:
        if text[r] == u'，' and r - mid > 10:
            break
        r += 1
        if r >= length:
            break

    return text[l + 1:r]


class AnalysisCore(object):
    def __init__(self):
        self.mapping = {u'外观': [u'外观', u'质感'], u'质量': [u'质量', u'品质'], u'物流': [u'物流', u'快递'], u'性价比': [u'性价比', u'实惠'],
                        u'材质': [u'材质', u'坚固', u'耐磨'], u'服务': [u'服务', u'卖家', u'态度']}
        self.misnoun = [u'感觉', u'有点', u'现象', u'生气']
        self.main_key = [u'质量', u'外观', u'服务', u'物流', u'性价比', u'舒适', u'色差', u'包装', u'气味', u'声音', u'颜色', u'效果', u'材质']
        self.result = {}
        self.data = []
        self.mainlist = []
        self.mainop = []
        self.corpus = ''
        self.textlist = []
        self.total_of_key = 0
        self.num_of_text = 0
        print 'Loading Word2vector Model'
        self.model = gensim.models.Word2Vec.load_word2vec_format(
            "CommentAnalysis\\management\\commands\\analysis\\result\\zhiwiki_big.vector")
        # self.model = gensim.models.Word2Vec.load_word2vec_format("result\\zhiwiki_big.vector")
        print 'Initialization Complete'

    def build_mainlist(self):
        num_of_key = 0
        fd = codecs.open("quality.dict", "w+", encoding="utf-8")
        for word in self.main_key:
            self.mainop.append(KeyUnit.keydata(num_of_key, word, 0, '', 0, -1, ''))
            num_of_key += 1
        for keyword in self.main_key:
            if keyword in self.mapping.keys():
                for item in self.mapping[keyword]:
                    self.mainlist.append(item)
                    fd.write(item + ' 1000\n')
            else:
                self.mainlist.append(keyword)
                fd.write(keyword + ' 1000\n')
        fd.close()
        jieba.load_userdict("quality.dict")

    def read_data(self, query):
        tdate = []
        trend_by_month = {}
        all_sentiment = []
        num_of_key = 0
        # for filename in glob(u"tbcomment\\*{}.txt".format(int(query))):
        for filename in glob(u"CommentAnalysis\\management\\commands\\analysis\\tbcomment\\*{}.txt".format(int(query))):
            stdin = open(filename, 'r+')
            while 1:
                text_raw = stdin.readline().decode('utf-8')
                if len(text_raw) == 0:
                    break
                text, date = text_raw.split('\t', 1)
                date = date.strip()
                if len(text) < 8:
                    continue
                if date[-8:] in tdate:
                    continue
                tdate.append(date[-8:])
                month = parse_month(date)
                self.textlist.append(text)
                self.corpus = self.corpus + text
                # f2.write(text)
                stext = SnowNLP(text)
                text_sentiments = stext.sentiments
                textrank = phrase_extract.textrank(text, topK=5, withWeight=True, allowPOS=('n', 'a'))
                for keyword, weight in textrank:
                    sentence = locate(keyword, text, 0)
                    s_sentence = SnowNLP(sentence)
                    sentiment = s_sentence.sentiments
                    tmp = KeyUnit.keydata(num_of_key, keyword, weight, sentence, sentiment, self.num_of_text, date)
                    self.data.append(tmp)
                    num_of_key += 1
                if len(text) < 50:
                    sentences = re.split(u',|，|。|;|;| ', text)
                    for sentence in sentences:
                        if len(sentence) == 0:
                            continue
                        sentence = re.sub(
                            "[A-Za-z0-9\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\,\[\]\.\<\>\/\?\！\\\%]", "",
                            sentence)
                        noun = []
                        adj = []
                        for word, flag in pseg.cut(sentence):
                            if word in self.mainlist:
                                if word not in [w[0] for w in textrank]:
                                    r_sentence = locate(word, text, 0)
                                    s_sentence = SnowNLP(r_sentence)
                                    sentiment = s_sentence.sentiments
                                    tmp = KeyUnit.keydata(num_of_key, word, 0.8, r_sentence, sentiment,
                                                          self.num_of_text, date)
                                    self.data.append(tmp)
                                    num_of_key += 1
                                if flag == 'n':
                                    noun.append(word)
                            if flag == 'a' or flag == 'an' or flag == 'ad':
                                adj.append(word)
                        for n, a in itertools.product(noun, adj):
                            if abs(sentence.find(n) - sentence.find(a)) > 6:
                                continue
                            for item in self.mainop:
                                if self.mapping.has_key(item.keyword):
                                    if n in self.mapping[item.keyword]:
                                        if item.adjs.has_key(n + a):
                                            item.adjs[n + a] = item.adjs[n + a] + 1
                                        else:
                                            item.adjs[n + a] = 1
                                elif item.keyword == n:
                                    if item.adjs.has_key(n + a):
                                        item.adjs[n + a] = item.adjs[n + a] + 1
                                    else:
                                        item.adjs[n + a] = 1
                self.num_of_text += 1
                all_sentiment.append(text_sentiments)
                if month in trend_by_month.keys():
                    trend_by_month[month].append(text_sentiments)
                else:
                    trend_by_month[month] = [text_sentiments]
        stdin.close()
        for month in trend_by_month.keys():
            sentiment_array = np.array(trend_by_month[month])
            trend_by_month[month] = sentiment_array.mean()
        self.result['trend_by_month'] = trend_by_month
        self.total_of_key = num_of_key
        self.result['num_of_text'] = self.num_of_text
        self.result['all_sentiment'] = sum(all_sentiment) / self.num_of_text * 10
        self.result['keywords'] = []
        for cor_key, cor_weight in phrase_extract.textrank(self.corpus, topK=8, withWeight=True, allowPOS=('a')):
            if cor_weight > 0.1:
                self.result['keywords'].append(cor_key)

    def integrate_data(self):
        # mainop
        self.result['mainop'] = []
        candidate_list = [[0, 0] for i in range(6)]
        for item_a in self.mainop:
            # simmax = self.num_of_text / 2
            simlist = []
            if item_a.keyword in self.mapping.keys():
                simlist = self.mapping[item_a.keyword]
            else:
                simlist.append(item_a.keyword)
            for simkey in simlist:
                # simnum = 0
                for item_b in self.data:
                    if item_b.keyword not in self.model.vocab:
                        continue
                    if item_b.weight == 0:
                        continue
                    sim = self.model.similarity(simkey, item_b.keyword)
                    if sim > 0.7:
                        item_a.weight = item_a.weight + item_b.weight * sim
                        if sim > 0.9:
                            item_b.weight = 0
                        if item_b.textID[0] not in item_a.textID and sim > 0.8:
                            item_a.textID.append(item_b.textID[0])
                            item_a.sentence.append([item_b.sentence[0][0], item_b.date])
                        item_a.sentiment = item_a.sentiment + item_b.sentiment
                        item_a.num = item_a.num + 1
                        # simnum = simnum + 1
                        # if simnum > simmax:
                        # simmax = simnum
                        # item_a.keyword=simkey
            if item_a.num > 1:
                item_a.sentiment = item_a.sentiment / (item_a.num - 1)
            if item_a.weight > candidate_list[-1][1]:
                candidate_list[-1][0] = item_a.ID
                candidate_list[-1][1] = item_a.weight
            candidate_list = sorted(candidate_list, key=compair, reverse=True)
        for candidate in candidate_list:
            temp = self.mainop[candidate[0]]
            if temp.weight < self.num_of_text / 30:
                continue
            for adj in temp.adjs.keys():
                if temp.adjs[adj] <= 1:
                    del temp.adjs[adj]
            for i in range(len(temp.textID) - 1):
                temp.sentence[i] = [locate(temp.sentence[i + 1][0], self.textlist[temp.textID[i + 1]], 1),
                                    temp.sentence[i + 1][1]]
            del temp.sentence[-1]
            self.result['mainop'].append(temp.tran_to_dict())

        # otherop
        self.result['otherop'] = []
        simmap = [[0 for col in range(self.total_of_key)] for row in range(self.total_of_key)]
        for item_a in self.data:
            if item_a.keyword not in self.model.vocab:
                continue
            if item_a.weight == 0:
                continue
            if item_a.keyword in self.misnoun:
                continue
            flagg = 0
            pos = pseg.cut(item_a.keyword)
            for word, flag in pos:
                if flag == 'n':  # and simi(word,u'属性')>0.2:
                    flagg = 1
            if flagg == 0:
                continue
            for item_b in self.data:
                if item_b.keyword not in self.model.vocab:
                    continue
                if item_b.weight == 0:
                    continue
                sim = max(simmap[item_a.ID][item_b.ID], simmap[item_b.ID][item_a.ID])
                if sim == 0:
                    simmap[item_a.ID][item_b.ID] = self.model.similarity(item_a.keyword, item_b.keyword)
                    sim = simmap[item_a.ID][item_b.ID]
                if item_a.ID != item_b.ID and sim > 0.7:
                    # print item_a.keyword.encode('utf-8')+ ' ' +item_b.keyword.encode('utf-8')
                    item_a.weight = item_a.weight + item_b.weight * sim
                    if sim > 0.9:
                        item_b.weight = 0
                        if item_b.textID[0] not in item_a.textID:
                            item_a.textID.append(item_b.textID[0])
                            item_a.sentence.append([item_b.sentence[0][0], item_b.date])
                    item_a.sentiment = item_a.sentiment + item_b.sentiment
                    item_a.num = item_a.num + 1
            # print item_a.keyword.encode('utf-8')
            item_a.sentiment = item_a.sentiment / item_a.num
        candidate_list = [[0, 0] for i in range(6)]
        for item_a in self.data:
            if item_a.weight > candidate_list[-1][1]:
                candidate_list[-1][0] = item_a.ID
                candidate_list[-1][1] = item_a.weight
            candidate_list = sorted(candidate_list, key=compair, reverse=True)
        for candidate in candidate_list:
            temp = self.data[candidate[0]]
            if temp.weight < self.num_of_text / 20:
                continue
            for i in range(len(temp.textID)):
                temp.sentence[i] = [locate(temp.sentence[i][0], self.textlist[temp.textID[i]], 1), temp.sentence[i][1]]
            self.result['otherop'].append(temp.tran_to_dict())

    def analysis(self, query):
        self.result = {}
        self.data = []
        self.mainlist = []
        self.mainop = []
        self.corpus = ''
        self.textlist = []
        self.total_of_key = 0
        self.num_of_text = 0
        self.result['ID'] = query
        self.build_mainlist()
        try:
            self.read_data(query)
        except:
            self.result['error'] = 'read data error'
            return json.dumps(self.result)
        # try:
        self.integrate_data()
        # except:
        #    self.result['error'] = 'integrate data error'
        #    return json.dumps(self.result)
        return json.dumps(self.result)


if __name__ == '__main__':
    analyzer = AnalysisCore()
    print analyzer.analysis(536499893821)
