# Comment Analysis Program
This program's idea is E-shop Comment Analysis System. This is about how to serve for E-commerce companies.  

Shopping online is more and more popular today. People buy products and leave comments on big E-commerce platforms such as Amazon. Most E-commerce companies have E-shops on these platforms. Their products received many customer comments there and it was inefficient for them to get feedback about their products by manually reading the comments.  

So what they need is an assistant that could provide multi-dimensional comment analysis and extract customers¡¯ opinions.  

## Solution
The following flowchart will show how we analysis the comments. First our analysis server get the product¡¯s item ID on E-commerce platforms from ERP systems (B1). Then our comments extractor will extract the product¡¯s comments from the E-commerce platforms. Next, we use technology of TF-IDF, TextRank and POStag to mine keywords in the comments. These keywords will then be put into a similarity calculation unit. In this unit, we use a trained word2vec model to embed these keywords in a vector space. So that we can cluster the keywords with similar meanings as opinions by spectral clustering. Next, we do sentiment analysis toward each opinion. We use technology of word segmentation and Naive Bayes Classifier to quantify customers¡¯ sentiment according to their expressions on each opinion. To ensure the accuracy of this Naive Bayes Classifier as well as the word2vec model mentioned above, we collected corpus from Wiki and E-commerce platforms and labelled some of them. The labelled corpus are used to train the Naive Bayes Classifier and the labelled corpus are used to train Word2vec model. Finally, all the analysis result are returned to the ERP systems and displayed in one dashboard.  


## Codes and environment
The Django project folder attached includes the codes of comment analysis core, the raw comments of products in different categories on Tmall crawled before and the already trained word2vector file. If you want the original code of the web crawler and word2vec training, they are in the folder ¡®otherCode¡¯.  
To run the Django project, first you need to configure your environment to fulfill the requirements below.

### Requirements:

+ Python 2.7.12
+ Django 1.10
+ Python package:
..+ snownlp
..+ numpy
..+ jieba
..+ genism

### Recommended but not necessary:

+ Anaconda 4.1.1 32-bit, which includes the proper Python and Django version
+ Pycharm IDE, which is convenient to run Django.

### How To Run
After you configure the environment, go to the directory of _\DjangoCodes\CommentAnalysis_ and open the command line there. Input the followings:

```
python manage.py runserver 8000
python manage.py startanalysis
```

(If you use pycharm IDE, you need to open the folder as Django project and run it. And then find the terminal tab below and type ¡®python manage.py startanalysis¡¯)  
Once the server is on and the analysis server is listening, you can let it do comment analysis through _127.0.0.1:8000/CA/api?q=_ now. For example, if you want to analyze the comments of product whose ID is 536499893821, you can try _http://127.0.0.1:8000/CA/api?q=536499893821_ in your browser. Then you should get the JSON result just the same as the sample JSON file attached. Notice that the POC could only analyze the product whose comments we have already crawled, have a look at this folder ¡®¡­\PycharmProjects\CommentAnalysis\CommentAnalysis\management\commands\analysis\tbcomment¡¯ to know the available product ID.
