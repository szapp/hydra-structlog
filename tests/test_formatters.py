from dirty_equals import IsInstance
from structlog.stdlib import ProcessorFormatter

from hydra_structlog.formatters import build_processor_formatter


class CustomFormatter(ProcessorFormatter):
    pass


def test_build_processor_formatter_returns_initialized_formatter():
    """The formatter produces a valid structlog processor formatter."""
    inputs = [0]

    actual = build_processor_formatter(processors=inputs, foreign_pre_chain=[])

    assert actual == IsInstance(ProcessorFormatter)
    assert actual.processors == inputs


def test_build_processor_formatter_returns_custom_object():
    """The instantiation target is not overridden."""
    inputs = [0]

    actual = build_processor_formatter(
        _target_="tests.test_formatters.CustomFormatter",
        processors=inputs,
        foreign_pre_chain=[],
    )

    assert actual == IsInstance(CustomFormatter)
