from tag import TagProcessor
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

    def priority(self):
        return 60


class UpdateTags(UpdateHook):
    def name(self):
        return "tags"

    def update(self, note):
        processor = TagProcessor()
        return processor.update_tags(note)


class UpdateTagsBackpropagation(UpdateHook):
    def name(self):
        return "tags_backpropagation"

    def update(self, note):
        processor = TagProcessor()
        return processor.update_tags(note, backpropagation=True)
