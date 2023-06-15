import shutil
import pathlib
import os

import templates.index
import cuca_utils
from note import Note


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
            cuca_utils.write_file(index.path, templates.index.__doc__)

            return True
        except FileExistsError:
            return False

    def is_init(self):
        return os.path.isdir(self.cuca_data_dir())

    def get_all_files(self):
        return [f for f in os.listdir(self.path) if not f.startswith(".") and f.endswith(Note.EXT)]

    def empty_notes(self, files):
        empty = set()
        if len(files) == 0:
            files = self.get_all_files()

        for f in files:
            n = self.get_note(f)
            if n.empty():
                empty.add(n.get_file_title())
        return empty

    def get_note(self, title):
        return Note(os.path.join(self.path, Note.title_to_filename(title)))

    def get_all_notes(self):
        return [self.get_note(f) for f in self.get_all_files()]

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

    def contains(self, title):
        path = os.path.join(self.path, Note.title_to_filename(title))
        return os.path.exists(path)
