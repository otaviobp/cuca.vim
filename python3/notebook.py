import shutil
import pathlib
import os

from collections.abc import Mapping
import cuca_utils
from note import Note


class Notebook(Mapping):
    INDEX = "index"

    def __init__(self, path="."):
        self._path = os.path.realpath(path)

    def __getitem__(self, key):
        return Note(self._path, key)

    def __contains__(self, key):
        if isinstance(key, Note):
            note = key
            dirname = os.path.realpath(os.path.dirname(note._path))
            if self._path != dirname:
                return False
        else:
            note = self[key]

        return note.exists()

    def __iter__(self):
        for f in os.listdir(self._path):
            if not f.startswith(".") and f.endswith(Note.EXT):
                yield Note.key_from_path(f)

    def __len__(self):
        return len(list(self.__iter__()))

    def __eq__(self, other):
        return self._path == other._path

    @staticmethod
    def from_note(note):
        return Notebook(os.path.dirname(note._path))

    def init(self):
        try:
            os.makedirs(self.cuca_data_dir())
            pathlib.Path(self.cuca_data_dir(".keep")).touch()
            index = self[Notebook.INDEX]
            self.overwrite_note(index, Note.create_header(Note.decorate_title(index.key())))

            return True
        except FileExistsError:
            return False

    def is_init(self):
        return os.path.isdir(self.cuca_data_dir())

    def new_file(self, title):
        note = Note(self._path, title)
        if not note.exists():
            self.overwrite_note(note, Note.create_header(title))

        return note.path()

    def cuca_data_dir(self, *args):
        return os.path.join(self._path, ".cuca", *args)

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

    def overwrite_note(self, note, content):
        lines = [x + "\n" for x in content]
        f = open(note._path, "w")
        f.writelines(lines)
        f.close()
