import os

# Naming conventions
# title: Decorated title used on note (ex: 'Teste')
# sanitized_title: Title on note, but sanitized. Should be identical to
#                  file_title (ex: 'teste')
# filename: name of the file with extension (ex: 'teste.cuca'
# file_title: name of the file without extension (ex: 'teste')
# path: Full path of the file


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
    def title_to_filename(title):
        filename = Note.sanitize_title(title)
        if filename.endswith(Note.EXT):
            return filename
        return filename + Note.EXT

    @staticmethod
    def filename_to_title(filename):
        if filename.endswith(Note.EXT):
            return filename[:-3]

        return filename

    @staticmethod
    def header_sep(size):
        return Note.HEADER_SEP_CHAR * size

    @staticmethod
    def decorate_title(title):
        title = Note.sanitize_title(title)
        return " ".join([x.capitalize() for x in title.split("_")])

    def __init__(self, path):
        self.path = path
        self._lines = None

    def lines(self):
        if self._lines is None:
            f = open(self.path, "r")
            self._lines = [x[:-1] for x in f.readlines()]
            f.close()

        return self._lines

    # Get line without linebreak.
    # Return empty string if line doesn't exist
    def line(self, num):
        lines = self.lines()
        if num >= len(lines):
            return ""

        return lines[num]

    def get_title(self):
        return self.line(0)

    def get_sanitized_title(self):
        return Note.sanitize_title(self.get_title())

    def get_file_title(self):
        return os.path.basename(self.path)[: -(len(Note.EXT))]

    def get_file_title_decorated(self):
        return " ".join(
            [x.capitalize() for x in os.path.basename(self.path)[: -(len(Note.EXT))].split("_")]
        )

    def empty(self):
        if len(self.lines()) > 3:
            return False

        return self.check_header()

    def check_header(self):
        title, header, blank = self.line(0), self.line(1), self.line(2)
        f_title = self.get_file_title()
        sanitized_title = Note.sanitize_title(title)

        if f_title != sanitized_title:
            return False

        if header != Note.header_sep(len(title)) or blank != "":
            return False

        return True
