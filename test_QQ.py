import os

import pytest
import allure_pytest

def test_addition():
    assert 1 + 1 == 2

def test_subtraction():
    assert 5 - 3 == 2

def test_failure():
    # 这个测试会失败，用于演示
    assert 1 + 1 == 2
