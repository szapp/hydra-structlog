import logging

import pytest
from dirty_equals import IsAnyStr

from hydra_structlog.init import exception_logger, warning_logger


def test_warning_logger_logs_warning(caplog: pytest.LogCaptureFixture):
    """Warnings are formatted and emitted in log."""
    with caplog.at_level(logging.WARNING, "test_init"):
        warning_logger("TestWarning", UserWarning, "filename", 42)

    assert caplog.record_tuples == [
        (IsAnyStr(), logging.WARNING, "UserWarning: TestWarning (line 42)")
    ]


def test_exception_logger_logs_exception(caplog: pytest.LogCaptureFixture):
    """Exceptions are formatted and emitted in log."""
    with caplog.at_level(logging.CRITICAL):
        exception_logger(Exception, Exception("test"), None)

    assert caplog.record_tuples == [("exception", logging.CRITICAL, "test")]


@pytest.mark.parametrize(
    ["filename", "skip"],
    [
        pytest.param("hydra/core/utils.py", True, id="skip_file"),
        pytest.param("path/to/other.py", False, id="keep_file"),
    ],
)
def test_exception_logger_logs_trimmed_traceback(
    caplog: pytest.LogCaptureFixture, filename: str, skip: bool
):
    """Traceback skips frames from hydra but keeps other frames."""

    # Raise an exception a few frames deep
    def deep_raise():
        raise RuntimeError("test")

    # Construct a frame with a specific file name
    code = compile(
        "deep_raise()",
        filename=filename,
        mode="exec",
    )

    # Run the nested code to create a traceback
    try:
        exec(code, {"deep_raise": deep_raise})
    except RuntimeError as exc:
        tb = exc.__traceback__

    with caplog.at_level(logging.CRITICAL):
        exception_logger(Exception, Exception("test"), tb)

    assert (filename in str(caplog.get_records("call")[0].exc_text)) is not skip


def test_exception_logger_logs_user_interrupt(caplog: pytest.LogCaptureFixture):
    """KeyboardInterrupt exceptions are logged as simple errors."""
    with caplog.at_level(logging.ERROR):
        exception_logger(KeyboardInterrupt, KeyboardInterrupt("test"), None)

    assert caplog.record_tuples == [
        ("exception", logging.ERROR, IsAnyStr(regex=".*interrupt.*"))
    ]
