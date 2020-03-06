
import pytest

def test_failed(record_xml_attribute):
    record_xml_attribute("auto_case", "False")
    record_xml_attribute("CPU","50%")
    record_xml_attribute("MEM", "450MB")
    assert True

def test_failed2(record_xml_attribute):
    record_xml_attribute("auto_case","True")
    record_xml_attribute("CPU", "60%")
    record_xml_attribute("MEM", "200MB")
    assert False

def test_failed3(record_property):
    record_property("50","400")
    assert False
