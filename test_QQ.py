# test_sample.py
import pytest
def test_addition():
    assert 1 + 1 == 2, "1加1应该等于2"

def test_string():
    assert "hello".upper() == "HELLO"