import shutil
import pathlib
import os
import re

import cuca_utils
from note import Note
from note_parser import NoteParser


class Notebook:
    INDEX = "index"
    INDEX_FILE = INDEX + Note.EXT

    def __init__(self, path="."):
        self.path = path

    @staticmethod
    def from_note(note):
        return Notebook(os.path.dirname(note.path))

    def init(self):
        try:
            os.makedirs(self.cuca_data_dir())
            pathlib.Path(self.cuca_data_dir(".keep")).touch()
            index = self.get_note("Index")
            pathlib.Path(index.path).touch()
            NoteFixer(index).fix_all()

            return True
        except FileExistsError:
            return False

    def is_init(self):
        return os.path.isdir(self.cuca_data_dir())

    def all_files(self):
        return [f for f in os.listdir(self.path) if not f.startswith(".") and f.endswith(Note.EXT)]

    def empty_notes(self, files):
        empty = set()
        if len(files) == 0:
            files = self.all_files()

        for f in files:
            n = self.get_note(f)
            if n.empty():
                empty.add(n.get_file_title())
        return empty

    def get_note(self, title):
        return Note(os.path.join(self.path, Note.title_to_filename(title)))

    def get_all_notes(self):
        return [self.get_note(f) for f in self.all_files()]

    def new_file(self, title):
        filename = Note.title_to_filename(title)

        if not os.path.exists(filename):
            f = open(filename, "w")
            sep = "=" * len(title)
            f.write(title + "\n")
            f.write(sep + "\n\n")
            f.close()

        return filename

    def cuca_data_dir(self, *args):
        return os.path.join(self.path, ".cuca", *args)

    def add_file(self, path, title=""):
        base, ext = os.path.splitext(path)
        if title == "":
            title = os.path.basename(base)
            title = Note.decorate_title(title)

        ftype = cuca_utils.guess_filetype(path)
        if ftype.startswith("image/"):
            basedir = "imgs"
        else:
            basedir = "files"

        fdir = self.cuca_data_dir(basedir)
        os.makedirs(fdir, exist_ok=True)

        dest = os.path.join(fdir, Note.sanitize_title(title) + ext)
        dest = cuca_utils.gen_unique_path(dest)

        shutil.copy(path, dest)

        return dest, title


class NoteFixer:
    def __init__(self, note):
        self.note = note

    def __fix_header(self):
        # If header is valid
        if (
            len(self.note.lines()) >= 2
            and len(self.note.line(1)) > 0
            and self.note.line(1) == Note.header_sep(len(self.note.line(1)))
        ):
            if self.note.get_sanitized_title() != self.note.get_file_title():
                self.note._lines[0] = self.note.get_file_title_decorated()
            if self.note.line(1) != Note.header_sep(len(self.note.line(0))):
                self.note._lines[1] = Note.header_sep(len(self.note.line(0)))
            return

        if self.note.get_sanitized_title() != self.note.get_file_title():
            self.note._lines.insert(0, self.note.get_file_title_decorated())
        self.note._lines.insert(1, Note.header_sep(len(self.note.line(0))))

    def __fix_header_empty_line(self):
        if len(self.note.lines()) == 2 or self.note.line(2) != "":
            self.note._lines.insert(2, "")

    def __fix_heading_spacing(self):
        i = 0
        while i < len(self.note._lines):
            l = self.note._lines[i]
            if l.startswith("#"):
                index = cuca_utils.index_not_char(l, "#")
                if index < len(l) and l[index] != " ":
                    self.note._lines[i] = l[:index] + " " + l[index:]

                # Needs to add line breaks
                if self.note._lines[i - 1] != "":
                    self.note._lines.insert(i, "")
                    i = i + 1

                if i + 1 < len(self.note._lines) and self.note._lines[i + 1] != "":
                    self.note._lines.insert(i + 1, "")

            i = i + 1

    def __fix_heading_promote(self):
        def should_promote():
            for x in self.note.lines():
                if x.startswith("# "):
                    return True
            return False

        if not should_promote():
            return

        i = 0
        while i < len(self.note._lines):
            l = self.note._lines[i]
            if l.startswith("#"):
                self.note._lines[i] = "#" + l
            i = i + 1

    def __fix_wild_file_urls(self):
        def create_link_to_file_url(match):
            title = os.path.splitext(os.path.basename(match.group(1)))[0]
            title = Note.decorate_title(title)

            notebook = Notebook.from_note(self.note)
            dest, title = notebook.add_file(match.group(1), title)
            basedir = os.path.basename(os.path.dirname(dest))
            basename = os.path.basename(dest)
            dest = os.path.join(basedir, basename)

            return "[{}]({}){}".format(title, dest, match.group(2))

        pattern_file_url = NoteParser().pattern_file_url

        i = 0
        while i < len(self.note._lines):
            self.note._lines[i] = re.sub(
                pattern_file_url, create_link_to_file_url, self.note._lines[i]
            )
            i = i + 1

    def __fix_wild_urls(self):
        def create_link_to_url(match):
            title = cuca_utils.get_title_from_url(match.group(1))

            return "[{}]({}){}".format(title, match.group(1), match.group(2))

        pattern_url = NoteParser().pattern_url

        i = 0
        while i < len(self.note._lines):
            self.note._lines[i] = re.sub(pattern_url, create_link_to_url, self.note._lines[i])
            i = i + 1

    def fix_all(self):
        self.__fix_header()
        self.__fix_header_empty_line()
        self.__fix_heading_spacing()
        self.__fix_heading_promote()
        self.__fix_wild_urls()
        self.__fix_wild_file_urls()

        # Save File
        lines = [x + "\n" for x in self.note.lines()]
        f2 = open(self.note.path, "w")
        f2.writelines(lines)
        f2.close()
