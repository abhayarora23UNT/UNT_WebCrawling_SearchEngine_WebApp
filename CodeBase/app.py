# Import Statements #
import requests
from bs4 import BeautifulSoup           # python libary to parse html pages #
from indexingvector import vectorSpaceModel  # importing methods from another python file name indexing vector
from flask import Flask, render_template, request, redirect, url_for # python library to build web application
from corpusCrawler import extractCorpusFromLinks  # importing methods from another python file name corpusCrawler
import time                              # python methods to suspend execution of threads

viewHeader="University Of North Texas Search"
app = Flask(__name__)                    # Flask constructor takes the name of current module

@app.route("/", methods=["GET", "POST"])
def index():                            # Python decorator that Flask provides to assign URLs in our app
    if request.method == 'POST':
        query = request.form['search']
        return redirect(url_for('search', query=query))
    else:
        return render_template("index.html", title=viewHeader)

        
@app.route("/<query>")                   # Python decorator that Flask provides to assign URLs in our app
def search(query):

    if not query:
        return redirect(url_for('index'))
    else:
        results = vectorSpaceModel(query)

        outputs = []

        for result in results:
            link = result.get('link')
            link = link.replace(" ", "")
            doc = result.get('doc')
            title = doc.split("|")[0]
            try:
                description = doc.split("|")[1]
            except:
                description = "No description"

            if len(title) > 100:
                title = title[:100] + "..."

            if len(description) > 500:
                description = description[500:1000] + "..."

            class Obj:
                def __init__(self, title, link, description):
                    self.title = title
                    self.url = link
                    self.description = description

            output = Obj(title, link, description)
            outputs.append(output)

    return render_template("index.html", title="University Of North Texas Search", query=query, results=outputs)


# Method Not Used #
def getInternalLinks(page_url, allLinksCollection, pageLinksSet): 
    """ Method to get internal links.
    """
    for link in allLinksCollection:
        if "href" in link.attrs:
            if link.attrs["href"] not in pageLinksSet:  # checking if link already added in set , to avoid duplicates #
                internalLinkUrl = link.attrs["href"]
                print("debug: getInternalLinks")
                print(internalLinkUrl)
                pageLinksSet.add(internalLinkUrl)
                getInternalLinks(internalLinkUrl, allLinksCollection, pageLinksSet)
        else :
            pass


@app.route("/webCrawler", methods=["GET", "POST"])  # Python decorator that Flask provides to assign URLs in our app
def webCrawler():
    # print("debug: ",request.method)
    seedUrl="https://unt.edu"
    hostUrl="unt.edu"
    crawlFilePath="allCrawlLinks.txt"
    try:
        with open(crawlFilePath, "r", encoding="utf-8") as f:
            linksUrl = f.readlines() # reading data from file
        f.close()
    except:
        linksUrl = []

    corpus = extractCorpusFromLinks()  # call method to update Corpus

    print("debug: linksUrl")
    print(linksUrl)
    return render_template("index.html", title=viewHeader, links=linksUrl)

    # Below Code Snippet not used #
     
    # if request.method == 'POST':
    #     responseObj = requests.get(seedUrl, timeout=25)
    #     htmlContent = responseObj.text
    #     print("debug: webCrawler")
    #     print(htmlContent)  # print statements for Debugging #
    #     soup = BeautifulSoup(htmlContent, "html.parser")

    #     pageLinksSet= set()  # initialize set #      
    #     allLinksCollection= soup.findAll('a', href=lambda href: href and hostUrl in href and "mailto" not in href) 
    #     print("debug: LengthCheck", len(allLinksCollection))
    #     getInternalLinks("", allLinksCollection, pageLinksSet)
    #     time.sleep(3)

    #     print("debug: pageLinksSet")
    #     print(pageLinksSet)     # print statements for Debugging #
        
      
    #     with open(crawlFilePath, "w", encoding="utf-8") as f:
    #         f.write("")  # emptying the files #

    #     with open(crawlFilePath, "w", encoding="utf-8") as f:
    #         for item in pageLinksSet:
    #             f.write(item + "\n")  # appending each link from set to text file 
    #     f.close()

    #     with open(crawlFilePath, "r", encoding="utf-8") as f:
    #         linksUrl = f.readlines()  # reading data from file 
    #     f.close()

    #     return render_template("index.html", title=viewHeader, links=linksUrl)  # render html view #
    # else:
    #     print("In else app.py")
    #     try:
    #         with open(crawlFilePath, "r", encoding="utf-8") as f:
    #             linksUrl = f.readlines() # reading data from file
    #         f.close()
    #     except:
    #         linksUrl = []

    #     corpus = extractCorpusFromLinks()

    #     print("debug: linksUrl")
    #     print(linksUrl)
    #     return render_template("index.html", title=viewHeader, links=linksUrl)



