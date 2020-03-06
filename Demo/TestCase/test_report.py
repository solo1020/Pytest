import pytest

def test_success():
    """this test succeeds"""
    assert True

def test_failure():
    assert False

def test_skip():
    pytest.skip('for a reason!')

def test_broken():
    raise Exception('oops')

