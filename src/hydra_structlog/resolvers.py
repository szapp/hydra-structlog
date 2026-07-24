import os


def dev_switch(is_dev, is_not_dev, *, _root_):
    """OmegaConf resolver to select node based on dev environment."""
    # Grab ENV from 'env_set' first and fall back to environment variable
    hydra_env = _root_.get("hydra", {}).get("job", {}).get("env_set", {})
    ENV = hydra_env.get("ENV", os.environ.get("ENV")) or "dev"
    return is_dev if ENV == "dev" else is_not_dev
