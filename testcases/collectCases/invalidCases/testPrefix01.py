# _*_ coding: utf-8 _*_
# @File : testPrefix01.py
# @Author : isquz
# @Time : 2020/8/29 13:30 
# @desc :

def test_out_of_Testclass():
    assert True

def testOut_of_Testclass():
    assert True

def out_of_Testclass_test():
    assert True

def out_of_Testclasstest():
    assert True

def between_test_out_of_TestClass():
    assert True


class Testclass():

    def testIn_Testclass(self):
        assert True

    def test_in_Testclass(self):
        assert True

    def in_Testclass_test(self):
        assert True

    def in_Testclasstest(self):
        assert True

class clsTest():

    def testIn_non_Testclass(self):
        assert True

    def test_in_non_Testclass(self):
        assert True

    def in_non_Testclass_test(self):
        assert True

    def in_non_Testclasstest(self):
        assert True