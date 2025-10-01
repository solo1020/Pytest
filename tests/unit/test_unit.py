# _*_ coding: utf-8 _*_
# @Author: quzheng
# @Date: 2025/10/1 9:50
# @Desc:
# pytest-demo/tests/unit/test_unit.py

import pytest


def test_with_fixture(setup_unit):
    """
    使用 unit 目录定义的 fixture
    """
    print(f"执行 test_with_fixture，收到 fixture 数据: {setup_unit}")
    # 访问全局参数（推荐方式）
    param = pytest.config.param if hasattr(pytest, 'config') else None
    if param is None:
        # 更安全的方式是通过 request
        pass
    print(f"🌍 参数信息: {param}")


def test_simple():
    """简单测试函数"""
    print("执行 test_simple")


def test_with_request(request):
    """
    推荐方式：通过 request 获取 config
    """
    param = request.config.param
    env = getattr(request.config, 'test_env', 'N/A')
    print(f"参数: {param}, 环境: {env}")