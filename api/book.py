from flask import Flask, Response, jsonify, render_template
from base64 import b64encode
import feedparser
import re

import requests
import json
import os
import random

GOODREADS_RSS_URL = os.getenv("GOODREADS_RSS_URL")

PROGRESS_REGEX = r".*<img .* alt=\"([^\"]*) by ([^\"]*)\".*src=\"([^\"]*)\".*.* is on page ([0-9]*) of ([0-9]*) of <a.*"
READ_REGEX = r".*<img .* alt=\"([^\"]*) by ([^\"]*)\".*src=\"([^\"]*)\".*"

def loadImageB64(url):
    resposne = requests.get(url)
    return b64encode(resposne.content).decode("ascii")

def makeSVG(book, author, progress, img_url):
    img = loadImageB64(img_url)

    dataDict = {
        "progress": progress,
        "author": author,
        "book_name": book,
        "img": img,
    }

    return render_template("goodreads.html.j2", **dataDict)


app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def last_activity(path):
    activityFeed = feedparser.parse(GOODREADS_RSS_URL)
    data = ""
    entries = activityFeed.entries
    pr = re.compile(PROGRESS_REGEX)
    rr = re.compile(READ_REGEX)
    for i in entries:
        i["summary"] = i["summary"].replace("&lt;","<").replace("&gt;",">").replace("&quot;","\"").replace("\n","")
        res = pr.search(i["summary"])
        if res:
            book, author, img = res.group(1,2,3)
            progress = int(100*int(res.group(4))/int(res.group(5)))
        else:
            res = rr.search(i["summary"])
            if res:
                book, author, img = res.group(1,2,3)
                progress = 100
            else:
                continue
        svg = makeSVG(book, author, progress, img)
        resp = Response(svg, mimetype="image/svg+xml")
        resp.headers["Cache-Control"] = "s-maxage=1"
        return resp
    return data

if __name__ == "__main__":
    app.run(debug=True)

