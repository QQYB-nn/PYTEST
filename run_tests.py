
import os
import pytest
import sys

if __name__ == '__main__':
    pytest.main(['test_QQ.py', '--alluredir=./allure-results', '-v'])

    # 使用 os.system 生成报告（不推荐）
    os.system('allure generate ./allure-results -o ./allure-report --clean')
    os.system('allure open ./allure-report')