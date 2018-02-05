# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 17:54:00 2016

@author: I334169

Before this, you should
-read the comments and zhwiki-latest-pages-articles.xml.bz2(downloaded from internet) using this package: 'from gensim.corpora import WikiCorpus'
-transform it to simplified Chinese, get rid of the symbols (  'sentence = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", sentence)'  )
-save to txt
"""

from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import multiprocessing


def my_function():
    a = open('reduce_zhiwiki.txt', 'r')
    f_1 = open('result//zhiwiki_big.model', 'w')
    f_2 = open('result//zhiwiki_big.vector', 'w')
    model = Word2Vec(LineSentence(a), size=50, window=5, min_count=5, workers=multiprocessing.cpu_count()-1)
    model.save(f_1)
    model.save_word2vec_format(f_2, binary=False)
if __name__ == '__main__':
    my_function()