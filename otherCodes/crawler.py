# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 15:31:26 2016

@author: I334169

Crawl product comments through categories in Tmall.
Need to create a new folder named tbcomment first!
"""

from selenium import webdriver
import re
from time import clock
import os.path
import glob

false=0
true=1
stime=clock()

driver_item = webdriver.Chrome()
driver_item.get('https://www.taobao.com/markets/tbhome/market-list')
page_item=driver_item.page_source
categories=re.findall('<a class="category-name".*?>(.*?)</a>',page_item)
for item in categories:
    if len(glob.glob(u"C:\\Users\\I334169\\Documents\\python\\tbcomment\\"+item+'*'))>0:
        continue
    driver_search = webdriver.Chrome()
    item=re.sub("[0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", item)
    path="tbcomment\\"+item
    pages=[0]
    print item
    for s in pages:
        driver_search.get("https://s.taobao.com/search?q="+item+"&fs=1&filter_tianmao=tmall"+"&s="+str(s))
        page=driver_search.page_source
        nids=re.findall('"nid":"(.*?)"',page)
        userids=re.findall('"user_id":"(.*?)"',page)
        driver2 = webdriver.PhantomJS()
        for i in range(len(nids)):
            if os.path.exists(path+str(nids[i])+".txt"):
                break
            f=open(path+str(nids[i])+".txt","w")    
            #print "crawlling itemID:"+str(nids[i])        
            for j in range(6):
                url="https://rate.tmall.com/list_detail_rate.htm?itemId="+str(nids[i])+"&sellerId="+str(userids[i])+"&order=3&currentPage="+str(j)   
                driver2.get(url)
                page=driver2.page_source
                comments=re.findall('"rateContent":"(.*?)","rateDate":"(.*?)"',page)            
                for comment in comments:
                    f.write(comment[0].encode('utf-8')+'\t'+comment[1].encode('utf-8')+'\n')
            f.close()
        driver2.quit()
    driver_search.quit()
ftime=clock()
print ftime-stime
