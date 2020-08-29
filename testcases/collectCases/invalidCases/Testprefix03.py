# _*_ coding: utf-8 _*_
# @File : Testprefix03.py
# @Author : isquz
# @Time : 2020/8/29 13:47 
# @desc : 非 test_ 前缀的均无法被收集为case

def test_out_of_Testclass3():
    assert True

def testOut_of_Testclass3():
    assert True

def out_of_Testclass3_test():
    assert True

def out_of_Testclass3test():
    assert True

def between_test_out_of_TestClass3():
    assert True


class Testclass3():

    def testIn_Testclass3(self):
        assert True

    def test_in_Testclass3(self):
        assert True

    def in_Testclass3_test(self):
        assert True

    def in_Testclass3test(self):
        assert True

class cls3Test():

    def testIn_non_Testclass3(self):
        assert True

    def test_in_non_Testclass3(self):
        assert True

    def in_non_Testclass3_test(self):
        assert True

    def in_non_Testclass3test(self):
        assert True