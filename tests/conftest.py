# _*_ coding: utf-8 _*_
# @Author: quzheng
# @Date: 2025/10/1 9:50
# @Desc:
# pytest-demo/tests/conftest.py
# 作用：tests 目录下的 conftest，第二层加载

import pytest
from _pytest.config import Config


def pytest_configure(config: Config):
    """
    4. tests 目录的配置初始化
    执行时机：在 root conftest 的 pytest_configure 之后执行
    """
    print(f"\n[TESTS conftest] 当前参数: {getattr(config, 'param', 'None')} (继承自 root)")
    config.test_env = "integration"


def pytest_runtest_setup(item):
    """
    7. 每个测试函数运行前调用
    执行时机：测试执行阶段
    """
    print(f"\n[TESTS conftest] 测试前准备: {item.name}")


def pytest_runtest_teardown(item, nextitem):
    """
    8. 每个测试函数运行后调用
    """
    print(f"\n[TESTS conftest] 清理测试: {item.name}")