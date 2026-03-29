from hydra.utils import instantiate
from structlog.stdlib import ProcessorFormatter

from .init import init_plugin


def build_processor_formatter(**kwargs) -> ProcessorFormatter:
    """Dynamically instantiate the processor chain from plain logging config."""
    kwargs.setdefault("_target_", "structlog.stdlib.ProcessorFormatter")
    processor = instantiate(kwargs)
    init_plugin(processor.foreign_pre_chain)
    return processor
