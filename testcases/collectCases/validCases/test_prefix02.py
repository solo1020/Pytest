# _*_ coding: utf-8 _*_
# @File : test_prefix02.py
# @Author : isquz
# @Time : 2020/8/29 13:37 
# @desc : test_ 前缀文件中： test开头的函数可以识别

def test_out_of_Testclass2():
    assert True

def testOut_of_Testclass2():
    assert True

def out_of_Testclass2_test():
    assert True

def out_of_Testclass2test():
    assert True

def between_test_out_of_TestClass2():
    assert True


class Testclass2():

    def testIn_Testclass2(self):
        assert True

    def test_in_Testclass2(self):
        assert True

    def in_Testclass2_test(self):
        assert True

    def in_Testclass2test(self):
        assert True

class cls2Test():

    def testIn_non_Testclass2(self):
        assert True

    def test_in_non_Testclass2(self):
        assert True

    def in_non_Testclass2_test(self):
        assert True

    def in_non_Testclass2test(self):
        assert True
