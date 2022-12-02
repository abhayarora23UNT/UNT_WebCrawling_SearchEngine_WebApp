import os
import re
from bs4.element import Comment
import requests
from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import urllib.request
import time


def cleanText(element):
    if element.parent.name in ['style','script','head','title','meta','[document]']:
        return False
    if isinstance(element, Comment):
        return False

    return True

def extractCorpusFromLinks():
    with open("allCrawlLinks.txt", "r", encoding="utf-8") as f:
        links = f.readlines()
    f.close()

    temp_database = []

    for link in links:
        try:   
            

            response=requests.get(link)
            if response.status_code==429:
                time.sleep(int[response.headers["Retry-After"]])
            else:
                html=urllib.request.urlopen(link).read()
                soup = BeautifulSoup(html, 'html.parser')
              
                

            # f = urllib.request.urlopen('http://www.python.org/')
            # html = f.read().decode('utf-8')
            # print(html) 
            # headersVal = {
            #     'User-Agent': "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            # }
            # r = requests.get(link, headers=headersVal,timeout=10 )
            # print("status code is", r.status_code, "  " , link)
            # if r.status_code == 404:
            #     continue
            # soup = BeautifulSoup(r.content, 'html.parser')
            # if soup.title:
            #     print("Here",soup.title)
            #     if "Page not found" in soup.title.text:
            #         print("Page not found")
            #         continue

            class Obj:
                def __init__(self, link, soup):
                    self.link = link
                    self.soup = soup
            result = Obj(link, soup)
            print(" Appending links ", link)
            temp_database.append(result)
        except Exception as e:
            print('Invalid link')
            print(e)
            pass
    f.close()
    print(temp_database)
    corpus = []
    for obj in temp_database:
        link = obj.link
        soup = obj.soup
        text =  soup.get_text()
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        # allTexts=soup.findAll(text=True)
        # text =  filter(cleanText,allTexts)
        # text=u" ".join(t.strip() for t in text)
        text = text.replace('\n', ' ')
        text = ' '.join(text.split())

        class Obj:
            def __init__(self, link, text):
                self.link = link
                self.text = text
        result = Obj(link, text)
        corpus.append(result)

    try:
        os.remove("corpus.txt")
    except:
        pass

    print("corpus", len(corpus))
    with open("corpus.txt", "w", encoding="utf-8") as f:
        for obj in corpus:
            f.write("Link:{}Doc:{}\n".format(obj.link, obj.text))
    f.close()

    return corpus
