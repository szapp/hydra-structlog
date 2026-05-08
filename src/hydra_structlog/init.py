import logging
import os
import sys
import warnings
from collections.abc import Sequence
from types import TracebackType
from typing import Any, TextIO

import structlog

# Original warnings.showwarning and sys.excepthook
_showwarning = None
_excepthook = None
_configured_once = False


def warning_logger(
    message: Warning | str,
    category: type[Warning],
    filename: str,
    lineno: int,
    file: TextIO | None = None,
    line: str | None = None,
) -> None:
    """Emit Python-native warnings as logging warnings."""
    frame = sys._getframe(2)
    module = frame.f_globals.get("__name__")
    logger = logging.getLogger(module)
    logger.warning("%s: %s (line %d)", category.__name__, message, lineno)


def exception_logger(
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_traceback: TracebackType | None,
) -> Any:
    """Exception hook to log uncaught exceptions."""
    logger = logging.getLogger("exception")

    if issubclass(exc_type, KeyboardInterrupt):
        logger.error("User interrupt")
        return

    # Skip Hydra frames in stack trace (see hydra._internal.utils.run_and_report)
    skip_files = (
        "hydra/core/utils.py",  # hydra
        "hydra_zen/wrapper/_implementations.py",  # hydra-zen
        "hydra/main.py",  # hydra through hydra-zen
        "pydantic/_internal/_validate_call.py",  # hydra-zen with pydantic wrapper
    )
    try:
        tb = exc_traceback
        while tb is not None:
            frame = tb.tb_frame
            tb = tb.tb_next
            filename = frame.f_code.co_filename.replace(os.sep, "/")
            if filename.endswith(skip_files) and tb:
                exc_traceback = tb
    except Exception:  # pragma: no cover
        pass

    message = getattr(exc_value, "message", str(exc_value))
    exc_info = exc_type, exc_value, exc_traceback
    logger.critical(message, exc_info=exc_info)


def init_plugin(
    foreign_pre_chain: Sequence[structlog.typing.Processor],
) -> None:  # pragma: no cover
    """Configure structlog and warning and exception hooks."""
    global _excepthook, _showwarning, _configured_once

    if _showwarning is None:
        _showwarning = warnings.showwarning
        warnings.showwarning = warning_logger  # type: ignore[ty:invalid-assignment]

    if _excepthook is None:
        os.environ["HYDRA_FULL_ERROR"] = "1"  # Suppress Hydra's exception hook
        _excepthook = sys.excepthook
        sys.excepthook = exception_logger

    if _configured_once is False:
        structlog.configure(
            processors=(
                list(foreign_pre_chain)
                + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter]
            ),
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
        _configured_once = True
