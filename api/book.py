import requests
from flask import Flask, Response, render_template, request
from base64 import b64encode
import feedparser
import re

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


PROGRESS_REGEX = r".*<img .* alt=\"([^\"]*) by ([^\"]*)\".*src=\"([^\"]*)\".*.* is on page ([0-9]*) of ([0-9]*) of <a.*"
READ_REGEX = (
    r".*<img .* alt=\"([^\"]*) by ([^\"]*)\".*src=\"([^\"]*)\".*finished reading.*"
)


def loadImageB64(url):
    resposne = requests.get(url)
    return b64encode(resposne.content).decode("ascii")


def makeSVG(books):
    return render_template("goodreads.html.j2", books=books)


class Book:
    def __init__(self, title, author, img_url):
        self.title = title
        self.author = author
        self.img = ""
        if img_url != "":
            self.img = loadImageB64(img_url)

    def __eq__(self, other):
        return self.title == other.title and self.author == other.author


app = Flask(__name__)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def last_activity(path):
    goodread_rss_url = (
        f'https://www.goodreads.com/user/updates_rss/{request.args.get("id")}'
    )
    print(goodread_rss_url)
    activityFeed = feedparser.parse(goodread_rss_url)
    entries = activityFeed.entries
    pr = re.compile(PROGRESS_REGEX)
    rr = re.compile(READ_REGEX)
    books = []

    for i in entries:
        i["summary"] = (
            i["summary"]
            .replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&quot;", '"')
            .replace("\n", "")
        )
        res = pr.search(i["summary"])

        if res:
            title, author, img = res.group(1, 2, 3)
            book = Book(title, author, img)
            if book not in books:
                books.append(book)
            # progress = int(100 * int(res.group(4)) / int(res.group(5)))
        else:
            res = rr.search(i["summary"])
            if res:
                title, author, img = res.group(1, 2, 3)
                book = Book(title, author, img)
                if book not in books:
                    books.append(book)
                # progress = 100
            else:
                continue

        if len(books) >= request.args.get("maxbooks", 3):
            break
    svg = makeSVG(books)
    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-Control"] = "s-maxage=1"
    return resp


if __name__ == "__main__":
    app.run(debug=True)
