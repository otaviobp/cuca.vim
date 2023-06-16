import re

from notebook import Notebook
from note_parser import NoteParser
from note import Note


class Tag:
    PREFIX = "Tag: "
    PREFIX_SANITIZED = "tag_"

    def __init__(self, notebook, tag):
        if tag.startswith(Tag.PREFIX):
            tag = tag[len(Tag.PREFIX) :]
        self.tag = Note.sanitize_title(tag)

        self.notebook = notebook
        self.note = self.notebook[Tag.PREFIX + tag]
        self.children = self.__parse(self.note.lines())

    def __parse(self, lines):
        pattern_item = NoteParser.patterns().pattern_item
        notebook = Notebook.from_note(self.note)
        children = set()
        for line in lines:
            m = re.match(pattern_item, line)
            if m is not None:
                note = notebook[m.group(1)]
                if not note.key().startswith(Tag.PREFIX_SANITIZED):
                    children.add(note)

        return children

    def add(self, note):
        self.children.add(note)

    def lines(self):
        l = []
        l += Note.create_header(self.get_title())
        for note in sorted(list(self.children)):
            if note in self.notebook:
                title = str(note)
                l.append(" - [{}]".format(title))
        return l

    def get_title(self):
        return Tag.PREFIX + Note.decorate_title(self.tag)

    def __hash__(self):
        return hash(self.tag)

    def __lt__(self, other):
        return self.tag < other.tag

    def __eq__(self, other):
        return self.tag == other.tag

    def clean_children_backreference(self):
        parser = NoteParser()
        tag_prefix = Note.sanitize_title(Tag.PREFIX)

        new_children = set()
        for note in self.children:
            found = False
            for link in parser.parse_links(note.lines()):
                if Note.sanitize_title(link).startswith(tag_prefix):
                    if Note.sanitize_title(link) == self.note.key():
                        found = True
                        break

            if found:
                new_children.add(note)
        self.children = new_children


class TagProcessor:
    def update_tags(self, note, backpropagation=False):
        parser = NoteParser()
        tag_prefix = Note.sanitize_title(Tag.PREFIX)
        notebook = Notebook.from_note(note)

        tags = set()
        for link in parser.parse_links(note.lines()):
            if Note.sanitize_title(link).startswith(tag_prefix):
                tags.add(Tag(notebook, link))

        if backpropagation:
            for t in tags:
                t.clean_children_backreference()

        tags.add(Tag(notebook, "all"))
        for t in tags:
            t.add(note)
            notebook.overwrite_note(t.note, t.lines())

        return True
