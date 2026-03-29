from collections.abc import Callable, MutableMapping
from typing import Any

from structlog.typing import EventDict, WrappedLogger


class StaticFieldAdder:
    """Structlog processor to add static fields to all logs."""

    def __init__(self, **fields: str):
        self.fields = fields

    def __call__(
        self, logger: WrappedLogger, name: str, event_dict: EventDict
    ) -> EventDict:
        for field, value in self.fields.items():
            event_dict.setdefault(field, value)
        return event_dict


class FieldRenamer:
    """Structlog processor to rename fields. Existing fields of the new name are
    overwritten.
    """

    def __init__(self, **mapping: str):
        self.mapping = mapping

    def __call__(
        self, logger: WrappedLogger, name: str, event_dict: EventDict
    ) -> EventDict:
        for field, replace in self.mapping.items():
            if field in event_dict:
                event_dict[replace] = event_dict.pop(field)
        return event_dict


Processor = Callable[[Any, str, MutableMapping], MutableMapping]


def named_processor_chain(**processors: Processor) -> list[Processor]:
    """Convert a mapping of named processors into list. Skip None"""
    return [p for p in processors.values() if p is not None]
