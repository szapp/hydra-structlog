from hydra.core.plugins import Plugins
from hydra.plugins.search_path_plugin import SearchPathPlugin

from hydra_structlog.plugin import HydraStructlogSearchPathPlugin


def test_discovery() -> None:
    """Make sure plugin can be discovered after Plugins.register is called."""
    assert HydraStructlogSearchPathPlugin.__name__ in [
        x.__name__ for x in Plugins.instance().discover(SearchPathPlugin)
    ]
