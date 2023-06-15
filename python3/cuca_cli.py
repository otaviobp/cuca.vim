import os
import errno
from collections.abc import Mapping

from notebook import Notebook, NoteFixer
from hook_list import HookList
from note_parser import NoteParser
from note import Note
from cuca_gen import NoteHtmlGen
from commands import CLICommander


class HookCLI(Mapping):
    def __init__(self, func, hooks):
        self.func = func
        self.hooks = hooks

    def __getitem__(self, key):
        if key == "":
            return self.list
        return lambda args: self.func(self.hooks[key], *args)

    def list(self):
        for r in self.hooks:
            print(r)

    def __len__(self):
        return len(self.hooks) + 1

    def __iter__(self):
        yield ""
        yield from self.hooks.keys()

    def __contains__(self, k):
        return k == "" or k in self.hooks.keys()


class CucaCLI:
    def __init__(self):
        self.notebook = Notebook()
        self.hook_list = HookList()

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

    def filter_run(self, hook, *params):
        for n in sorted(hook.filter(self.notebook.get_all_notes(), *params)):
            print(n)

    def filter_remove(self, hook, *params):
        filtered_notes = sorted(hook.filter(self.notebook.get_all_notes(), *params))
        if len(filtered_notes) == 0:
            return

        for n in filtered_notes:
            print(n)

        if self.comfirm("Remove files?"):
            for n in filtered_notes:
                os.unlink(n.path)

    def main(self, args):
        cmd = CLICommander(
            "cuca",
            {
                "init": self.cuca_init,
                "filter": HookCLI(self.filter_run, self.hook_list.get_filter_hooks()),
                "fix": self.fix,
                "html": self.generate_html,
                "broken_links": self.broken_links,
                "broken_links_complete": self.broken_links_complete,
                "remove": HookCLI(self.filter_remove, self.hook_list.get_filter_hooks()),
            },
        )

        return cmd.run(args[1:])
