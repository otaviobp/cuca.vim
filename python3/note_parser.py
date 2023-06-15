import re


class NoteParser:
    def __init__(self):
        # Pattern to filter all URL links
        # self.pattern_link_url = re.compile(r'\[(?P<link>.*?)\]\((?P<url>.*?)\)')

        self.pattern_links = re.compile(r"\[(?P<link>.*?)\](?!\()")
        self.pattern_url = re.compile(r"(http[s]?:[^\)]*?)(\s|$)")
        self.pattern_file_url = re.compile(r"file://([^\)]*)?(\s|$)")

    def parse_links(self, lines):
        for line in lines:
            for x in re.findall(self.pattern_links, line):
                if x != "":
                    yield x

    def parse_urls(self, lines):
        for line in lines:
            for x in re.findall(self.pattern_url, line):
                if x != "":
                    yield x
