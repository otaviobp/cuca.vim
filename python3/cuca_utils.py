from urllib.request import Request, urlopen
from html.parser import HTMLParser
import mimetypes
import os


def __urlGetTitle(url):
    class ParseTitle(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.in_title = False
            self.title = ""
            self.title = ""
            self.done = False

        def handle_starttag(self, tag, attrs):
            if tag == "title":
                self.in_title = True
                self.title = ""

        def handle_endtag(self, tag):
            self.in_title = False
            if tag == "title":
                self.done = True

        def handle_data(self, data):
            if self.in_title:
                self.title = data

    if ":" not in url:
        url = "https://" + url

    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})

        parser = ParseTitle()
        response = urlopen(req)
        parser.feed(response.read().decode("utf-8"))

        return parser.title

    except Exception:
        return ""


def get_title_from_url(url):
    title = __urlGetTitle(url)
    title = title[:50].strip(" ")
    if title == "":
        title = "link"

    return title


def write_readonly_file(path, content):
    try:
        os.unlink(path)
    except FileNotFoundError:
        pass

    f = open(path, "w")
    f.writelines(content)
    f.close()

    permissions = os.stat(path).st_mode
    permissions &= ~0o222
    os.chmod(path, permissions)


def write_file(path, content):
    f = open(path, "w")
    f.writelines(content)
    f.close()


def index_not_char(string, c):
    """Return the index of the first char that is not equal 'c'"""

    for i in range(len(string)):
        if string[i] != c:
            return i
    return len(string)


def guess_filetype(path):
    ftype = mimetypes.guess_type(path)[0]
    if ftype is None:
        return "unknown"

    return ftype


def gen_unique_path(path):
    if not os.path.exists(path):
        return path

    counter = 0
    split_path = os.path.splitext(path)
    while os.path.exists(path):
        counter += 1
        path = split_path[0] + "_" + str(counter) + split_path[1]

    return path
