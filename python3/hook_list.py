from filter_hooks import FilterEmpty, FilterString, FilterUnreachable, FilterInvalidHeader
from hook import FilterHook, SearchHook, UpdateHook
from search_hooks import SearchBrokenLinks, SearchWildUrlLinks, SearchUrlLinks
from update_hooks import UpdateFix, UpdateHtml
from hook_external import ExternalFilterHook, ExternalSearchHook, ExternalUpdateHook


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
            # Update
            UpdateFix(),
            UpdateHtml(),
        ]

        # Look for user hooks
        self.hooks += ExternalFilterHook.find_hooks_on_path()
        self.hooks += ExternalSearchHook.find_hooks_on_path()
        self.hooks += ExternalUpdateHook.find_hooks_on_path()

    def get_filter_hooks(self):
        return {x.name(): x for x in self.hooks if isinstance(x, FilterHook)}

    def get_search_hooks(self):
        return {x.name(): x for x in self.hooks if isinstance(x, SearchHook)}

    def get_update_hooks(self):
        return {x.name(): x for x in self.hooks if isinstance(x, UpdateHook)}

    def get_update_hooks_priority_list(self):
        return sorted([x for x in self.hooks if isinstance(x, UpdateHook)])
