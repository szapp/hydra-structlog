# Hydra-Structlog

[![CI](https://github.com/szapp/hydra-structlog/actions/workflows/ci.yml/badge.svg)](https://github.com/szapp/hydra-structlog/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/hydra-structlog)](https://pypi.python.org/pypi/hydra-structlog)
[![Python Versions](https://img.shields.io/pypi/pyversions/hydra-structlog)](https://github.com/szapp/hydra-structlog)
[![Support on Ko-fi](https://img.shields.io/badge/ko--fi-support-ff586e?logo=kofi&logoColor=white)](https://ko-fi.com/szapp)

An opinionated hydra plugin to configure logging with structlog.

## Usage

Structlog is fully integrated in Hydra through a config group named `structlog` for `hydra.job_logging`.

1. Install the plugin.

    ```sh
    uv add hydra-structlog
    ```

2. Override the job logging with a default in your config.

    ```yaml
    defaults:
      - override hydra/job_logging=structlog
    ```

3. Hydra will now emit JSON logs (by default to `structured.log`) and print human readably logs to the console.

## Customization

Structlog comes configured with opinionated defaults.

To adjust the processors, use the hydra defaults as outlined above and overwrite individual config entries afterwards.
For example:

```yaml
defaults:
  - override hydra/job_logging=structlog

# Change the storage location
hydra:
  job_logging:
    handlers:
      json:
        filename: ${hydra.runtime.cwd}/logs/structured.log
```

## Defaults

The configuration runs structlog through the standard library logging.
That has several advantages.

The use of structlog and logging, e.g. by third-party packages, are recorded and both exhibit structlog's bound contextvars.

The processor chain is conveniently exposed in the job_logging configuration and adjustable through hydra's config interface.

Because lists are not easily manipulated in hydra configs, the processor chains are defined as dictionaries.
The name of each processor does not matter as long as its unique in the chain.
The default processor chain can then be extended more comfortably.

To remove a processor set it to `null`. See example below.

Because structlog's ProcessorFormatter does not accept the processors as strings, the logging config contains `_target_` instantiation.

```yaml
defaults:
  - override hydra/job_logging=structlog

# Remove a processor from the default chain and add another one
hydra:
  job_logging:
    formatters:
      json:
        foreign_pre_chain:
          # Remove the add-log-level processor
          add_logger_name: null
          # Append a new processor
          arbitrary_name:
            # Follow hydra's instantiate syntax
            _target_: structlog.stdlib.add_log_level_number
            _partial_: true
```

## Notes

Python 3.14 is currently not supported as `hydra.main` causes a ValueError on argparse-validation, see <https://github.com/facebookresearch/hydra/issues/3121>.
It is recommended to use `hydra-zen` which does not have that problem and works well with Python 3.14.

Tracer injection is not implemented here as data science projects using hydra typically do not implement web apps.
Nevertheless, an appropriate structlog processor can be added to the job_logging config.
