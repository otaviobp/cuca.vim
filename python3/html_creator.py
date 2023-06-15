import markdown2
import os
import re
import cuca_utils

from note_parser import NoteParser
from note import Note
import templates.css


class HtmlCreator:
    def __init__(self, notebook):
        self.notebook = notebook
        self.html_dir = self.notebook.cuca_data_dir("html")
        if os.path.exists(self.html_dir):
            return

        os.makedirs(self.html_dir, exist_ok=True)
        cuca_utils.write_file(os.path.join(self.html_dir, "css.css"), templates.css.__doc__)
        os.symlink("../imgs", os.path.join(self.html_dir, "imgs"))
        os.symlink("../files", os.path.join(self.html_dir, "files"))

    def save_note_html(self, note):
        def create_link(match):
            title = match.group(1)
            return "[" + title + "](" + Note.sanitize_title(title) + ".html)"

        pattern_links = NoteParser().pattern_links

        lines = note.lines()
        i = 0
        while i < len(lines):
            lines[i] = re.sub(pattern_links, create_link, lines[i])
            i = i + 1

        txt = "\n".join(lines)
        html = markdown2.markdown(txt)

        # Save the file
        path = os.path.join(self.html_dir, note.get_file_title() + ".html")
        f = open(path, "w")
        f.writelines(["<html>", '<link rel="stylesheet" href="css.css">'])
        f.writelines(html)
        f.writelines("</html>")

        f.close()
