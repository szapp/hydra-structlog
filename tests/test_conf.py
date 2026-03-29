from hydra import initialize
from hydra.core.global_hydra import GlobalHydra


def test_config_installed() -> None:
    """Logging is available for both hydra/hydra_logging and hydra/job_logging."""

    with initialize("pkg://hydra_plugins.hydra_structlog.conf", version_base=None):
        config_loader = GlobalHydra.instance().config_loader()
        assert "structlog" in config_loader.get_group_options("hydra/job_logging")
