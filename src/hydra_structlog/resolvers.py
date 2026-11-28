import os
from typing import Any

from omegaconf import Container, OmegaConf


def dev_switch(is_dev: Any, is_not_dev: Any, *, _root_: Container) -> Any:
    """OmegaConf resolver to select node based on dev environment."""
    # Grab ENV from 'env_set' first and fall back to environment variable
    hydra_env = OmegaConf.select(_root_, "hydra.job.env_set", default={})
    ENV = hydra_env.get("ENV", os.environ.get("ENV")) or "dev"
    return is_dev if ENV == "dev" else is_not_dev
