import os
import errno

from cuca import Notebook, NoteParser, NoteFixer, Note
from cuca_gen import NoteHtmlGen
from commands import CLICommander


class CucaCLI:
    def __init__(self):
        self.notebook = Notebook()

    def lint(self, args=[]):
        files = args
        if len(files) == 0:
            files = self.notebook.all_files()

        for f in files:
            if not self.notebook.get_note(f).check_header():
                print("Header invalid:", f)

    def fix(self, args=[]):
        files = args
        if len(files) == 0:
            files = self.notebook.all_files()

        for f in files:
            NoteFixer(self.notebook.get_note(f)).fix_all()

    def generate_html(self, args):
        files = args
        if len(files) == 0:
            files = self.notebook.all_files()

        gen = NoteHtmlGen(self.notebook)
        for f in files:
            gen.save_note_html(f)

    def broken_links(self, args):
        files = args
        parser = NoteParser()
        broken = set()
        all_files = self.notebook.all_files()
        if len(files) == 0:
            files = all_files

        for f in files:
            for l in parser.parse_links(self.notebook.get_note(f).lines()):
                if Note.title_to_filename(l) not in all_files:
                    broken.add(l)
        for l in sorted(broken):
            print(l)

    def broken_links_complete(self, args):
        files = args
        parser = NoteParser()
        all_files = self.notebook.all_files()
        if len(files) == 0:
            files = all_files

        for f in files:
            broken = []
            n = self.notebook.get_note(f)
            for l in parser.parse_links(n.lines()):
                if Note.title_to_filename(l) not in all_files:
                    broken.append(l)
            if len(broken) > 0:
                print(n.get_title() + ":")
                for b in broken:
                    print(" >", b)
                print()

    def comfirm(self, prompt="Confirm?"):
        return input(prompt + " ").lower() == "y"

    def remove_unreachable_files(self):
        unreachable = self.notebook.unreachable_files()
        if len(unreachable) == 0:
            return

        for l in sorted(unreachable):
            print(l)
        if self.comfirm("Remove unreachable files?"):
            for i in unreachable:
                os.unlink(self.notebook.get_note(i).path)

    def unreachable_files(self, _):
        for l in sorted(self.notebook.unreachable_files()):
            print(l)

    def remove_empty(self, args):
        files = args
        empty = self.notebook.empty_notes(files)
        if len(empty) == 0:
            return

        for l in sorted(empty):
            print(l)
        if self.comfirm("Remove empty files?"):
            for i in empty:
                os.unlink(self.notebook.get_note(i).path)

    def empty(self, args):
        files = args
        for l in sorted(self.notebook.empty_notes(files)):
            print(l)

    def help(self, params):
        print("help message")

    def invalid_command(self, params):
        print("Invalid Command: ", " ".join(params))

    def cuca_init(self):
        if self.notebook.is_init():
            print("This directory is already a cuca notebook")
            return errno.EEXIST

        if not self.notebook.init():
            print("Error on creating a notebook in current directory")
            return errno.EFAULT

    def bla(self, args):
        print("run> ", args)

    def main(self, args):
        cmd = CLICommander(
            "cuca",
            {
                "init": self.cuca_init,
                "lint": self.lint,
                "fix": self.fix,
                "html": self.generate_html,
                "broken_links": self.broken_links,
                "broken_links_complete": self.broken_links_complete,
                "unreachable_files": self.unreachable_files,
                "empty": self.empty,
                "remove": {
                    "unreachable_files": self.remove_unreachable_files,
                    "empty": self.remove_empty,
                },
                "bla": self.bla,
            },
        )

        return cmd.run(args[1:])
