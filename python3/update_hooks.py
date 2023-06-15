from html_creator import HtmlCreator
from notebook import Notebook
from note_fixer import NoteFixer
from hook import UpdateHook


class UpdateFix(UpdateHook):
    def name(self):
        return "fix"

    def update(self, note):
        NoteFixer(note).fix_all()
        return True


class UpdateHtml(UpdateHook):
    def name(self):
        return "html"

    def update(self, note):
        creator = HtmlCreator(Notebook.from_note(note))
        creator.save_note_html(note)
        return True
