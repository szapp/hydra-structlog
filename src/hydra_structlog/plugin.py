from hydra.core.config_search_path import ConfigSearchPath
from hydra.plugins.search_path_plugin import SearchPathPlugin
from omegaconf import OmegaConf

from .resolvers import dev_switch


class HydraStructlogSearchPathPlugin(SearchPathPlugin):
    def manipulate_search_path(self, search_path: ConfigSearchPath) -> None:
        OmegaConf.register_new_resolver("hydra-structlog.dev", dev_switch)
        search_path.append("hydra-structlog", "pkg://hydra_structlog.conf")
