from abc import abstractmethod, ABC


class Hook(ABC):
    def __lt__(self, other):
        if self.priority == other.priority:
            return self.name() < other.name()

        return self.priority() < other.priority()

    @abstractmethod
    def name(self):
        return ""

    def priority(self):
        return 50

    def __str__(self):
        return self.name()


class FilterHook(Hook):
    @abstractmethod
    def filter(self, notes, *params):
        return []


class SearchHook(Hook):
    @abstractmethod
    def search(self, note, *params):
        return []


class UpdateHook(Hook):
    @abstractmethod
    def update(self, note):
        return False
