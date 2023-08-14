import re
import os
import cuca_utils

from notebook import Notebook
from note import Note
from note_parser import NoteParser


class NoteFixer:
    def __init__(self, note):
        self.note = note
        self.notebook = Notebook.from_note(note)
        self.lines = list(note.lines())

    def __fix_header(self):
        # If header is valid
        if (
            len(self.lines) >= 2
            and len(self.lines[1]) > 0
            and self.lines[1] == Note.header_sep(len(self.lines[1]))
        ):
            if Note.sanitize_title(self.note.get_header_title()) != self.note.key():
                self.lines[0] = Note.decorate_title(self.note.key())
            if self.lines[1] != Note.header_sep(len(self.lines[0])):
                self.lines[1] = Note.header_sep(len(self.lines[0]))
            return

        if (
            len(self.lines) == 0
            or Note.sanitize_title(self.note.get_header_title()) != self.note.key()
        ):
            self.lines.insert(0, Note.decorate_title(self.note.key()))
        self.lines.insert(1, Note.header_sep(len(self.lines[0])))

    def __fix_header_empty_line(self):
        if len(self.lines) == 2 or self.lines[2] != "":
            self.lines.insert(2, "")

    def __fix_spacing_between_headers(self):
        i = 0
        while i < len(self.lines):
            l = self.lines[i]
            if l.startswith("#"):
                index = cuca_utils.index_not_char(l, "#")
                if index < len(l) and l[index] != " ":
                    self.lines[i] = l[:index] + " " + l[index:]

                # Needs to add line breaks
                if self.lines[i - 1] != "":
                    self.lines.insert(i, "")
                    i = i + 1

                if i + 1 < len(self.lines) and self.lines[i + 1] != "":
                    self.lines.insert(i + 1, "")

            i = i + 1

    def __fix_heading_promote(self):
        i = 0
        while i < len(self.lines):
            l = self.lines[i]
            if l.startswith("# "):
                self.lines[i] = "#" + l
            i = i + 1

    def __fix_wild_file_urls(self):
        def create_link_to_file_url(match):
            title = os.path.splitext(os.path.basename(match.group(1)))[0]
            title = Note.decorate_title(title)

            dest, title = self.notebook.add_file(match.group(1), title)
            basedir = os.path.basename(os.path.dirname(dest))
            basename = os.path.basename(dest)
            dest = os.path.join(basedir, basename)

            return "[{}]({}){}".format(title, dest, match.group(2))

        pattern_file_url = NoteParser.patterns().pattern_file_url

        i = 0
        while i < len(self.lines):
            self.lines[i] = re.sub(pattern_file_url, create_link_to_file_url, self.lines[i])
            i = i + 1

    def __fix_wild_urls(self):
        def create_link_to_url(match):
            title = cuca_utils.get_title_from_url(match.group(1))

            return "[{}]({}){}".format(title, match.group(1), match.group(2))

        pattern_wild_url = NoteParser.patterns().pattern_wild_url

        i = 0
        while i < len(self.lines):
            self.lines[i] = re.sub(pattern_wild_url, create_link_to_url, self.lines[i])
            i = i + 1

    def fix_all(self):
        self.__fix_header()
        self.__fix_header_empty_line()
        self.__fix_spacing_between_headers()
        self.__fix_heading_promote()
        self.__fix_wild_urls()
        self.__fix_wild_file_urls()

        if "\n".join(self.lines) != "\n".join(self.note.lines()):
            self.notebook.overwrite_note(self.note, self.lines)
