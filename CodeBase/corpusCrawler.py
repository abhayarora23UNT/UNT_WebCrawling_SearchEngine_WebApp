
# import statements # 

from bs4 import BeautifulSoup           # python libary to parse html pages #
import urllib.request                   # python module to handle opening of http urls #
from bs4.element import Comment
import requests                         
from flask import Flask, render_template, request, redirect, url_for
import time                             # python methods to suspend execution of threads
import os                               # Allows to run command in python script #
import re                               # import statement for regular expressions #
import json

def cleanText(htmlContent):
    """ Method to extract visible texts from html content.
    """
    if htmlContent.parent.name in ['style','script','head','title','meta','[document]']:
        return False
    if isinstance(htmlContent, Comment):
        return False

    return True

def extractCorpusFromLinks():
    """ Method to extract corpus list of document content from crawl url.
    """
    crawlFilePath="allCrawlLinks.txt"
    with open(crawlFilePath, "r", encoding="utf-8") as f:
        allLinksCollection = f.readlines() # reading data from file
    f.close()

    corpusCrawlDataList = []

    for link in allLinksCollection:
        try:   
            response=requests.get(link)
            if response.status_code==429:
                time.sleep(int[response.headers["Retry-After"]])
            else:
                html=urllib.request.urlopen(link).read()
                soupTagRef = BeautifulSoup(html, 'html.parser')
              
            class DataObj:
                def __init__(self, link, soupTagRef):
                    self.link = link
                    self.soupTagRef = soupTagRef
            result = DataObj(link, soupTagRef)

            print("debug: Appending links ", link)
            corpusCrawlDataList.append(result)  # appending dataObj to corpusCrawlDataList

        except Exception as e:
            print('debug: Link Crawl Exception: ')
            print(e)
            pass
    
    f.close()
    print("debug: corpusCrawlDataList")
    print(corpusCrawlDataList)
    
    cleanCorpusList=getRefinedCorpusList(corpusCrawlDataList)
    return cleanCorpusList  # return list

def getRefinedCorpusList(corpusCrawlDataList):
    """ Method to generate refineCorpusList.
    """
    corpusFilePath="corpusInfo.txt"
    refineCorpusList = []
    for item in corpusCrawlDataList:
        link = item.link
        soupTagRef = item.soupTagRef
        textContent =  soupTagRef.get_text()
        # textContent =  soupTagRef.get_text(strip=True)
        textContent = re.sub(r'[^\x00-\x7F]+', ' ', textContent)   # regex to replace non-ascii with space
        # allTexts=soupTagRef.findAll(text=True)
        # textContent =  filter(cleanText,allTexts)
        # textContent=u" ".join(t.strip() for t in text)
        textContent = textContent.replace('\n', ' ')
        textContent = ' '.join(textContent.split())

        class DataObj:
            def __init__(self,link,textContent):
                self.link = link
                self.text = textContent
        result = DataObj(link, textContent)
        refineCorpusList.append(result)

    try:
        os.remove(corpusFilePath)  # clear existing contents of file
    except:
        pass

    print("refineCorpusList", len(refineCorpusList))

    jsonResult = []
    for item in refineCorpusList:
            jsonObj={}
            jsonObj['url']=item.link
            jsonObj['urlContent']=item.text
            jsonResult.append(jsonObj)
    jsonString = json.dumps(jsonResult)

    with open("corpusUnt.json", "w") as f1:
        f1.write(jsonString)     
        f1.close()
    
    with open(corpusFilePath, "w", encoding="utf-8") as f:
        for item in refineCorpusList:
            f.write("Link:{}Doc:{}\n\n".format(item.link, item.text))
    f.close()

    return refineCorpusList