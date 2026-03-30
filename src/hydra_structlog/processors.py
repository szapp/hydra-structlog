from collections.abc import Callable, MutableMapping, Sequence
from typing import Any

from structlog.typing import EventDict, WrappedLogger


class StaticKeyAdder:
    """Structlog processor to add static keys to all logs."""

    def __init__(self, **keys: str):
        self.keys = keys

    def __call__(
        self, logger: WrappedLogger, name: str, event_dict: EventDict
    ) -> EventDict:
        for key, value in self.keys.items():
            if value is not None and value != "":
                event_dict.setdefault(key, value)
        return event_dict


class KeyRenamer:
    """Structlog processor to rename keys. Existing keys of new name are overwritten."""

    def __init__(self, **mapping: str):
        self.mapping = mapping

    def __call__(
        self, logger: WrappedLogger, name: str, event_dict: EventDict
    ) -> EventDict:
        for key, replace in self.mapping.items():
            if key in event_dict:
                event_dict[replace] = event_dict.pop(key)
        return event_dict


class KeySorter:
    """Sort keys in events.

    Args:
        key_order: List of keys that should be rendered in this exact order. Missing
            keys will be added as None.
        drop_missing: When True, extra keys in key_order will be dropped rather than
            added as None.
    """

    def __init__(
        self, key_order: Sequence[str] | None = None, drop_missing: bool = False
    ):
        self._ordered_items = self._items_sorter(key_order, drop_missing)

    @staticmethod
    def _items_sorter(
        key_order: Sequence[str] | None, drop_missing: bool
    ) -> Callable[[EventDict], dict[str, object]]:
        """Return a function to sort items from an `event_dict`.

        Modified from `structlog.processors._items_sorter`.
        """
        # Use an optimized version for each case.
        if key_order:

            def ordered_items(event_dict: EventDict) -> dict[str, Any]:
                items = []
                for key in key_order:
                    value = event_dict.pop(key, None)
                    if value is not None or not drop_missing:
                        items.append((key, value))

                items += sorted(event_dict.items())

                return dict(items)

        else:

            def ordered_items(event_dict: EventDict) -> dict[str, Any]:
                return dict(sorted(event_dict.items()))

        return ordered_items

    def __call__(
        self, logger: WrappedLogger, name: str, event_dict: EventDict
    ) -> EventDict:
        return self._ordered_items(event_dict)


Processor = Callable[[Any, str, MutableMapping], MutableMapping]


def named_processor_chain(**processors: Processor) -> list[Processor]:
    """Convert a mapping of named processors into list. Skip None"""
    return [p for p in processors.values() if p is not None]
