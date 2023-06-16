import re


class NotePatterns:
    def __init__(self):
        # Pattern to filter all URL links
        self.pattern_link_url = re.compile(r"\[(?P<link>.*?)\]\((?P<url>.*?)\)")
        self.pattern_links = re.compile(r"\[(?P<link>.*?)\](?!\()")
        self.pattern_wild_url = re.compile(r"(http[s]?:[^\)]*?)(\s|$)")
        self.pattern_file_url = re.compile(r"file://([^\)]*)?(\s|$)")
        self.pattern_headers = re.compile(r"#.*$")
        self.pattern_item = re.compile(r" *- *\[(.*)\] *$")


class NoteParser:
    __patterns = None

    @staticmethod
    def patterns():
        if NoteParser.__patterns is None:
            NoteParser.__patterns = NotePatterns()
        return NoteParser.__patterns

    def parse_links(self, lines):
        for line in lines:
            for x in re.findall(self.patterns().pattern_links, line):
                if x != "":
                    yield x

    def parse_wild_urls(self, lines):
        for line in lines:
            for x in re.findall(self.patterns().pattern_wild_url, line):
                if x != "":
                    yield x

    def parse_link_urls(self, lines):
        for line in lines:
            for x in re.findall(self.patterns().pattern_link_url, line):
                if x != "":
                    yield x

    def parse_headers(self, lines):
        for i, line in enumerate(lines):
            if re.match(self.patterns().pattern_headers, line):
                yield i
