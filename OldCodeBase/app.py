import requests
from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
from spiderbot import spiderbot
from vsm import vsm
import time


app = Flask(__name__)


@app.route("/q/<query>")
def search(query):

    if not query:
        return redirect(url_for('index'))
    else:
        results = vsm(query)

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

    return render_template("index.html", title="Search for", query=query, results=outputs)


def getInternalLinks(page_url, all_links, pagelinks): 
    for link in all_links:
        if "href" in link.attrs:
            if link.attrs["href"] not in pagelinks:
                new_page = link.attrs["href"]
                print(new_page)
                pagelinks.add(new_page)
                getInternalLinks(new_page, all_links, pagelinks)



@app.route("/explorer", methods=["GET", "POST"])
def explorer():
    print(request.method)
    if request.method == 'POST':
        results = requests.get("https://unt.edu", timeout=25)
        html = results.text
        print("debug  "+html)
        soup = BeautifulSoup(html, "html.parser")
        pagelinks= set()
        
        # all_links= soup.findAll('a', href=lambda href: href and "unt.edu" in href ) 
        all_links= soup.findAll('a', href=lambda href: href and "unt.edu" in href and "mailto" not in href) 
        # all_links= soup.findAll('a', href=lambda href: href and "http" in href and "unt.edu" in href and "mailto" not in href) 
        print("LengthCheck", len(all_links))
        getInternalLinks("", all_links, pagelinks)
        # links = soup.find_all(
        #     "a", href=lambda href: href and "unt.edu" in href and "mailto" not in href)
        time.sleep(3)
        print(pagelinks)
        
        open("links.txt", "w").close()

        with open("links.txt", "r", encoding="utf-8") as f:
            test = f.readlines()

        print(test)
        with open("links.txt", "w", encoding="utf-8") as f:
            f.write("")

        with open("links.txt", "w", encoding="utf-8") as f:
            for link in pagelinks:
                f.write(link + "\n")
        f.close()

        with open("links.txt", "r", encoding="utf-8") as f:
            links = f.readlines()
        f.close()

        return render_template("explorer.html", title="Explorer", links=links)
    else:
        print("In else app.py")
        try:
            with open("links.txt", "r", encoding="utf-8") as f:
                links = f.readlines()
            f.close()
        except:
            links = []

        corpus = spiderbot()

        print(links)
        return render_template("explorer.html", title="Explorer", links=links)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        query = request.form['search']
        return redirect(url_for('search', query=query))
    else:
        return render_template("index.html", title="Search Engine")
