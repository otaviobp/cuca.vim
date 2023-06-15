from abc import abstractmethod, ABC


class Hook(ABC):
    def __lt__(self, other):
        return self.name() < other.name()

    @abstractmethod
    def name(self):
        return ""


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
