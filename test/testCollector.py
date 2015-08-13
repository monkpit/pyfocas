from __future__ import print_function
import unittest
# from nose.tools import raises
from nose.plugins.attrib import attr
from pyfocas.Collector import Collector
from pyfocas.Machine import Machine
from pyfocas.Driver import ExampleDriver
from datetime import datetime


class test_Collector(unittest.TestCase):
    """
    This class of tests asserts the functionality of the Collector module.
    """
    @classmethod
    def setup_class(cls):
        driver = ExampleDriver("./lib/Fwlib32.dll",
                               extradlls=["./lib/fwlibe1.dll"])
        machines = [Machine(driver=driver, ip="127.0.0.1")]
        cls.collector = Collector(reporter=reporterFunction,
                                  machines=machines)

    def test_Collector_has_machines_list(self):
        self.assertIsNotNone(self.collector.machines)

    def test_Collector_collect_returns_list_with_timestamp(self):
        data = self.collector.collect()
        self.assertTrue(isinstance(data, list))
        self.assertTrue(isinstance(data[0]["timestamp"], datetime))


def reporterFunction(machine):
    return machine.createDatum()
