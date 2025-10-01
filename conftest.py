# _*_ coding: utf-8 _*_
# @Author: quzheng
# @Date: 2025/10/1 9:49
# @Desc:
# pytest-demo/conftest.py
# 作用：根目录 conftest，最先加载

import json
import pytest
from _pytest.config import Config
from _pytest.nodes import Item


def pytest_addoption(parser):
    """
    1. 添加自定义命令行参数 --param
    执行时机：配置解析阶段最早调用
    """
    parser.addoption(
        "--param",
        action="store",
        default="{}",
        help="JSON 格式的参数，例如: --param '{\"env\": \"test\", \"debug\": true}'"
    )


def pytest_configure(config: Config):
    """
    2. 配置初始化完成后调用
    执行时机：在 pytest_addoption 之后
    """
    param_str = config.getoption("--param")
    try:
        config.param = json.loads(param_str)
        print(f"\n[ROOT conftest] 解析 --param: {config.param}")
    except json.JSONDecodeError as e:
        raise pytest.UsageError(f"--param 不是合法的 JSON: {e}")


def pytest_collection_modifyitems(config: Config, items: list[Item]):
    """
    3. 测试用例收集完成后调用
    执行时机：收集所有测试函数后
    """
    print(f"\n[ROOT conftest] 收集到 {len(items)} 个测试用例")
    for item in items:
        print(f"  -> {item.nodeid}")