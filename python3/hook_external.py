import subprocess
import os

from hook import FilterHook, SearchHook, UpdateHook


def _find_binaries_with_prefix(prefix):
    for path in os.environ["PATH"].split(os.pathsep):
        if not os.path.isdir(path):
            continue

        for filename in os.listdir(path):
            if filename.startswith(prefix) and os.access(os.path.join(path, filename), os.X_OK):
                yield os.path.join(path, filename)


def _split_binary_name_priority(binary):
    name, _ = os.path.splitext(os.path.basename(binary))
    name = name[len(ExternalFilterHook.PREFIX) :]

    name_split = name.split("-", 1)
    if len(name_split) == 2:
        try:
            priority = int(name_split[0])
            return name_split[1], priority
        except ValueError:
            pass
    return name, 50


class ExternalFilterHook(FilterHook):
    PREFIX = "cuca-filter-"

    def __init__(self, binary):
        self.binary = binary
        self.binname, self.binpriority = _split_binary_name_priority(self.binary)

    def name(self):
        return self.binname

    def priority(self):
        return self.binpriority

    def filter(self, notes, *params):
        # TODO: Set params on an ENV variable

        note_dict = {note.path(): note for note in notes}
        cmdline = [self.binary] + list(note_dict.keys())
        ret = subprocess.run(cmdline, stdout=subprocess.PIPE)
        if ret.returncode != 0:
            yield from []
            return

        for file in ret.stdout.decode().split("\n"):
            if file in note_dict:
                yield note_dict[file]

    @staticmethod
    def find_hooks_on_path():
        for x in _find_binaries_with_prefix(ExternalFilterHook.PREFIX):
            yield ExternalFilterHook(x)


class ExternalSearchHook(SearchHook):
    PREFIX = "cuca-search-"

    def __init__(self, binary):
        self.binary = binary
        self.binname, self.binpriority = _split_binary_name_priority(self.binary)

    def name(self):
        return self.binname

    def priority(self):
        return self.binpriority

    def search(self, note, *params):
        cmdline = [self.binary, note.path()] + list(params)
        ret = subprocess.run(cmdline, stdout=subprocess.PIPE)
        if ret.returncode != 0:
            yield from []
            return

        for x in ret.stdout.decode().split("\n"):
            yield x

    @staticmethod
    def find_hooks_on_path():
        for x in _find_binaries_with_prefix(ExternalSearchHook.PREFIX):
            yield ExternalSearchHook(x)


class ExternalUpdateHook(UpdateHook):
    PREFIX = "cuca-update-"

    def __init__(self, binary):
        self.binary = binary
        self.binname, self.binpriority = _split_binary_name_priority(self.binary)

    def name(self):
        return self.binname

    def priority(self):
        return self.binpriority

    def update(self, note, *params):
        cmdline = [self.binary, note.path()] + list(params)
        ret = subprocess.run(cmdline, stdout=subprocess.PIPE)
        return ret.returncode == 0

    @staticmethod
    def find_hooks_on_path():
        for x in _find_binaries_with_prefix(ExternalUpdateHook.PREFIX):
            yield ExternalUpdateHook(x)
