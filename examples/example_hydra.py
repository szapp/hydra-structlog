"""Example with hydra."""

import logging
import warnings

import hydra

logger = logging.getLogger(__name__)


def func() -> None:
    warnings.warn("This Python native warning is logged as 'warning'")
    raise ValueError("This exception renders nicely with rich")


@hydra.main(config_path=".", config_name="config", version_base=None)
def my_app(cfg) -> None:
    logger.info("Hello World!")
    func()


if __name__ == "__main__":
    my_app()
