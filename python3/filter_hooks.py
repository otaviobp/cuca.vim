from abc import abstractmethod

from notebook import Notebook
from note_parser import NoteParser
from hook import FilterHook


class SimpleFilter(FilterHook):
    def filter(self, notes, *params):
        for n in notes:
            if self.filter_note(n, *params):
                yield n

    @abstractmethod
    def filter_note(self, n, params):
        return False


class FilterEmpty(SimpleFilter):
    def filter_note(self, note, *params):
        return note.empty()

    def name(self):
        return "empty"


class FilterString(SimpleFilter):
    def filter_note(self, note, *params):
        s = " ".join(params).lower()

        if s in str(note).lower():
            return True

    def name(self):
        return "string"


class FilterUnreachable(FilterHook):
    def name(self):
        return "unreachable"

    def filter(self, notes, *params):
        if len(notes) == 0:
            yield from []
            return

        notebook = Notebook.from_note(next(iter(notes)))
        all_notes = set(notes)
        reachable = set([notebook[Notebook.INDEX]])
        pending = [notebook[Notebook.INDEX]]
        parser = NoteParser()

        while len(pending) > 0:
            note = pending.pop(0)
            if note not in all_notes:
                continue

            for link in parser.parse_links(note.lines()):
                link_note = notebook[link]
                if link_note not in reachable:
                    reachable.add(link_note)
                    pending.append(link_note)

        yield from all_notes - reachable


class FilterInvalidHeader(FilterHook):
    def name(self):
        return "invalid_header"

    def filter(self, notes, *params):
        for n in notes:
            if not n.check_header():
                yield n
