import pytest
from job import precondition_valid_settings


def test_precondition_valid_settings():
    with pytest.raises(AssertionError):
        precondition_valid_settings({"key1": ["val1", "val2"], "key2": []})
    precondition_valid_settings({"key1": ["val1", "2val"], "key1": []})
