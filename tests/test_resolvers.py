import pytest

from hydra_structlog.resolvers import dev_switch


@pytest.mark.parametrize(
    ["env", "expected"],
    [
        pytest.param("dev", 1, id="is_dev"),
        pytest.param("prod", 0, id="is_not_dev"),
    ],
)
def test_dev_switch_resolves_from_os_env(
    monkeypatch: pytest.MonkeyPatch, env: str, expected: int
):
    """The environment variable ENV is correctly recognized for the switch."""
    monkeypatch.setenv("ENV", env)
    actual = dev_switch(1, 0, _root_={})
    assert actual == expected


@pytest.mark.parametrize(
    ["env", "expected"],
    [
        pytest.param("dev", 1, id="is_dev"),
        pytest.param("prod", 0, id="is_not_dev"),
    ],
)
def test_dev_switch_resolves_from_env_set(env: str, expected: int):
    """The config-environment variable is correctly recognized for the switch."""
    cfg = {"hydra": {"job": {"env_set": {"ENV": env}}}}
    actual = dev_switch(1, 0, _root_=cfg)
    assert actual == expected


@pytest.mark.parametrize(
    ["env_var", "env_cfg", "expected"],
    [
        pytest.param("prod", "dev", 1, id="is_dev"),
        pytest.param("dev", "prod", 0, id="is_not_dev"),
    ],
)
def test_dev_switch_prefers_env_var(
    monkeypatch: pytest.MonkeyPatch, env_var: str, env_cfg: str, expected: int
):
    """The environment config take precedence."""
    monkeypatch.setenv("ENV", env_var)
    cfg = {"hydra": {"job": {"env_set": {"ENV": env_cfg}}}}
    actual = dev_switch(1, 0, _root_=cfg)
    assert actual == expected
