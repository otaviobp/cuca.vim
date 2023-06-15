from notebook import Notebook
from hook import SearchHook
from note_parser import NoteParser


class SearchBrokenLinks(SearchHook):
    def name(self):
        return "broken_links"

    def search(self, note, *params):
        notebook = Notebook.from_note(note)
        parser = NoteParser()
        for l in parser.parse_links(note.lines()):
            if not notebook.contains(l):
                yield (l)


class SearchWildUrlLinks(SearchHook):
    def name(self):
        return "wild_url_links"

    def search(self, note, *params):
        parser = NoteParser()
        for l in parser.parse_wild_urls(note.lines()):
            yield (l[0])


class SearchUrlLinks(SearchHook):
    def name(self):
        return "url_links"

    def search(self, note, *params):
        parser = NoteParser()
        for l in parser.parse_link_urls(note.lines()):
            yield (l[1])
