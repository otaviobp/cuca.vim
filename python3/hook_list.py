from filters import FilterEmpty, FilterString, FilterUnreachable, FilterInvalidHeader
from hook import FilterHook


class HookList:
    def __init__(self):
        self.hooks = [
            FilterEmpty(),
            FilterString(),
            FilterUnreachable(),
            FilterInvalidHeader(),
        ]

    def get_filter_hooks(self):
        return {x.name(): x for x in self.hooks if isinstance(x, FilterHook)}
