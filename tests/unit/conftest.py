# _*_ coding: utf-8 _*_
# @Author: quzheng
# @Date: 2025/10/1 9:50
# @Desc:
# pytest-demo/tests/unit/conftest.py
# 作用：最内层 conftest，第三层加载

import pytest
from _pytest.config import Config


def pytest_configure(config: Config):
    """
    5. unit 目录的配置初始化
    执行时机：在 tests/conftest.py 之后执行
    """
    print(f"\n[UNIT conftest] 当前环境: {getattr(config, 'test_env', 'unknown')}")
    config.unit_mode = True


@pytest.fixture(scope="function")
def setup_unit(request):
    """
    9. 定义仅在 unit 目录下可用的 fixture
    执行时机：当测试函数请求该 fixture 时
    """
    print("\n[UNIT conftest] fixture setup_unit 开始")
    yield "unit_data"
    print("[UNIT conftest] fixture setup_unit 结束")