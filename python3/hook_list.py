from filter_hooks import FilterEmpty, FilterString, FilterUnreachable, FilterInvalidHeader
from hook import FilterHook, SearchHook
from search_hooks import SearchBrokenLinks, SearchWildUrlLinks, SearchUrlLinks


class HookList:
    def __init__(self):
        self.hooks = [
            # Filters
            FilterEmpty(),
            FilterString(),
            FilterUnreachable(),
            FilterInvalidHeader(),
            # Search
            SearchBrokenLinks(),
            SearchWildUrlLinks(),
            SearchUrlLinks(),
        ]

    def get_filter_hooks(self):
        return {x.name(): x for x in self.hooks if isinstance(x, FilterHook)}

    def get_search_hooks(self):
        return {x.name(): x for x in self.hooks if isinstance(x, SearchHook)}
