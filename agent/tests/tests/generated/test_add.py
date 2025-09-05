import pytest

def add(a, b):
    return a + b

def test_add_simple():
    a, b = 2, 3
    result = add(a, b)
    assert result == 5

def test_add_negative():
    a, b = -1, -2
    result = add(a, b)
    assert result == -3




