import logging
from typing import Any, TextIO

try:  # pragma: no cover
    from tqdm.std import tqdm as std_tqdm  # type: ignore[ty:unresolved-import]

    TqdmClass = type[std_tqdm]
except ImportError:  # pragma: no cover
    std_tqdm: Any = None
    TqdmClass = None


class TqdmStreamHandler(logging.StreamHandler):  # pragma: no cover
    """Handler inheriting from StreamHandler to route logging stream through tqdm."""

    def __init__(
        self,
        stream: TextIO | None = None,
        tqdm_class: TqdmClass = std_tqdm,
    ):
        super().__init__(stream=stream)
        self.tqdm_class = tqdm_class

    if std_tqdm is not None:

        def emit(self, record: logging.LogRecord):
            try:
                msg = self.format(record)
                self.tqdm_class.write(msg, end=self.terminator, file=self.stream)  # type: ignore
                self.flush()
            except (KeyboardInterrupt, RecursionError, SystemExit):
                raise
            except Exception:  # noqa: BLE001
                self.handleError(record)
