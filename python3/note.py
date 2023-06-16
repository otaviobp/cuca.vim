import os
import functools


@functools.total_ordering
class Note:
    EXT = ".cuca"
    HEADER_SEP_CHAR = "="

    @staticmethod
    def sanitize_title(title):
        whitespace_symbols = "-_*[]{}/\\?,&;'\": "
        for w in whitespace_symbols:
            title = title.replace(w, " ")

        title = "_".join([x for x in title.split(" ") if x != ""])
        return title.lower()

    @staticmethod
    def key_from_path(path):
        basename, _ = os.path.splitext(os.path.basename(path))
        return Note.sanitize_title(basename)

    @staticmethod
    def header_sep(size):
        return Note.HEADER_SEP_CHAR * size

    @staticmethod
    def create_header(title):
        return (title, "=" * len(title), "")

    @staticmethod
    def decorate_title(title):
        title = Note.sanitize_title(title)
        return " ".join([x.capitalize() for x in title.split("_")])

    def __init__(self, basedir, title):
        self._key = Note.sanitize_title(title)
        self._path = os.path.join(basedir, self._key + Note.EXT)
        self._lines = None

    def key(self):
        return self._key

    def __lt__(self, other):
        return self.key() < other.key()

    def __eq__(self, other):
        return self._path == other._path

    def __hash__(self):
        return hash(self._path)

    def lines(self):
        if self._lines is None:
            try:
                f = open(self._path, "r")
                self._lines = tuple(x[:-1] for x in f.readlines())
                f.close()
            except FileNotFoundError:
                self._lines = tuple()

        return self._lines

    # Get line without linebreak.
    # Return empty string if line doesn't exist
    def line(self, num):
        lines = self.lines()
        if num >= len(lines):
            return ""

        return lines[num]

    def get_header_title(self):
        if len(self.lines()) > 0:
            return self.line(0)
        return Note.decorate_title(self.key())

    def empty(self):
        if not self.exists() or len(self.lines()) == 0:
            return True

        if len(self.lines()) > 3:
            return False

        return self.check_header()

    def exists(self):
        return os.path.exists(self._path)

    def check_header(self):
        title, header, blank = self.line(0), self.line(1), self.line(2)

        if self.key() != Note.sanitize_title(title):
            return False

        if header != Note.header_sep(len(title)) or blank != "":
            return False

        return True

    def __str__(self):
        return self.get_header_title()

    def __repr__(self):
        return "<Note {}>".format(self.key())

    def path(self):
        return self._path
