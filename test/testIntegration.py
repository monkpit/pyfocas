from __future__ import print_function
import unittest
import logging
from nose.plugins.attrib import attr

from FanucImplementation.DriverImplementations import Fanuc30iDriver
from Focas.Collector import Collector
from Focas.Machine import Machine

TEST_MACHINE_IP = "10.108.7.41"


@attr("integration")
class testMachineConnection(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        logging.basicConfig(level=logging.INFO)

    def test_Machine_integration(self):
        # write a description
        driver = Fanuc30iDriver("./lib/Fwlib32.dll",
                                extradlls=["./lib/fwlibe1.dll"])
        machineList = [Machine(driver=driver, ip=TEST_MACHINE_IP)]
        collector = Collector(reporter, machineList)
        data = collector.collect()
        try:
            data[0]["timestamp"]
            data[0]["blockNumber"]
            data[0]["activeTool"]
            data[0]["programName"]
            data[0]["oNumber"]
            data[0]["loads"]["S"]
            data[0]["loads"]["X"]
            data[0]["alarm"]
        except KeyError as e:
            self.fail("One or more of the data items were not collected: %s"
                      % e)


def reporter(machine):
    return machine.createDatum()
