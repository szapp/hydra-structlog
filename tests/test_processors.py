import pytest
from structlog.processors import add_log_level, dict_tracebacks

from hydra_structlog.processors import (
    KeyRenamer,
    KeySorter,
    StaticKeyAdder,
    named_processor_chain,
)


class TestStaticKeyAdder:
    def test_processor_adds_new_keys(self):
        """Static keys are added."""
        expected = {"field": "value"}
        processor = StaticKeyAdder(**expected)
        actual = processor(None, "", {})

        assert actual == expected

    def test_processor_does_not_overwrite_existing_keys(self):
        """If keys are already in events, they are not overwritten."""
        static_keys = {"field": "value"}
        inputs = {"field": "foo"}
        processor = StaticKeyAdder(**static_keys)
        actual = processor(None, "", inputs)

        assert actual == inputs

    def test_processor_ignores_empty_keys(self):
        """Skipping static keys is important to remove them from configuration."""
        static_keys = {"field1": None, "field2": ""}
        inputs = {}
        processor = StaticKeyAdder(**static_keys)
        actual = processor(None, "", inputs)

        assert actual == inputs


class TestKeyRenamer:
    def test_processor_renames_keys(self):
        """Keys are replaced and their value remains the same."""
        inputs = {"a": "value", "c": "foo"}
        expected = {"b": "value", "c": "foo"}

        processor = KeyRenamer(a="b")
        actual = processor(None, "", inputs)

        assert actual == expected

    def test_processor_skips_non_existing_keys(self):
        """Non-existing keys do not cause issues but are ignored."""
        inputs = {"a": "value"}

        processor = KeyRenamer(c="b")
        actual = processor(None, "", inputs)

        assert actual == inputs


class TestKeySorter:
    def test_processor_sorts_keys_alphabetically_without_specified_order(self):
        """Alphabetic sorting is automatic and easier than a specified ordering."""
        inputs = {"foo": "value1", "bar": "value2", "baz": "value3"}
        expected = ["bar", "baz", "foo"]

        processor = KeySorter()
        actual = processor(None, "", inputs)

        assert list(actual) == expected

    def test_processor_sorts_keys_by_specified_order(self):
        """The specified order overrides alphabetic sorting."""
        inputs = {"foo": "value1", "bar": "value2", "baz": "value3"}
        expected = ["baz", "foo", "bar"]

        processor = KeySorter(["baz", "foo", "bar"])
        actual = processor(None, "", inputs)

        assert list(actual) == expected

    @pytest.mark.parametrize(
        ["drop", "expected"],
        [
            pytest.param(True, ["foo"], id="true_drops"),
            pytest.param(None, ["bar", "foo"], id="false_keeps"),
        ],
    )
    def test_processor_handles_missing_keys(self, drop: bool, expected: list):
        """Creating missing keys might be desired or would otherwise confuse."""
        inputs = {"foo": "value1"}

        processor = KeySorter(["bar", "foo"], drop_missing=drop)
        actual = processor(None, "", inputs)

        assert list(actual) == expected

    def test_processor_keeps_missing_keys_by_default(self):
        """The default behavior needs to be ensured."""
        inputs = {"foo": "value1"}
        expected = ["bar", "foo"]

        processor = KeySorter(["bar", "foo"])
        actual = processor(None, "", inputs)

        assert list(actual) == expected


def test_named_processor_chain_produces_sequence():
    """The named-processor mapping is turned into a list ordered by mapping keys."""
    actual = named_processor_chain(z=add_log_level, a=dict_tracebacks)

    assert actual == [add_log_level, dict_tracebacks]


def test_named_processor_chain_produces_empty_sequence():
    """An empty config should not cause an error."""
    actual = named_processor_chain()

    assert actual == []
