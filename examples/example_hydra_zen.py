"""Example with hydra-zen and pydantic validation."""

import logging
import os
import warnings

from hydra.conf import HydraConf
from hydra_zen import store, zen
from hydra_zen.third_party.pydantic import pydantic_parser
from pydantic import FutureDate

logger = logging.getLogger(__name__)


def func() -> None:
    warnings.warn("This Python native warning is logged as 'warning'")
    raise ValueError("This exception renders nicely with rich")


@store(
    input_1="2199-12-31",
    name="default",
)
def my_app(input_1: FutureDate) -> None:
    logger.info("Hello %s!", input_1)
    func()


if __name__ == "__main__":
    os.environ.setdefault("ENV", "dev")
    os.environ.setdefault("SERVICE", "test-service")
    os.environ.setdefault("VERSION", "0.1.0")

    defaults = HydraConf().defaults + [{"override job_logging": "structlog"}]
    store(HydraConf(defaults=defaults))
    store.add_to_hydra_store()

    task = zen(my_app, instantiation_wrapper=pydantic_parser)
    task.hydra_main(config_path=".", config_name="default", version_base=None)
