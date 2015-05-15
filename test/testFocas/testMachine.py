from __future__ import print_function
import unittest
from nose.tools import raises
from nose.plugins.attrib import attr
from Focas.Machine import Machine
from Focas.Driver import ExampleDriver, FocasDriverBase
from FanucImplementation.DriverImplementations import Fanuc30iDriver

THREE_SIXTEEN = "10.108.7.41"


class testFocasExceptions(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        cls.driver = ExampleDriver("./lib/Fwlib32.dll",
                                   extradlls=["./lib/fwlibe1.dll"])
        cls.noNameMachine = Machine(driver=cls.driver, ip="127.0.0.1")
        cls.fullParamsMachine = Machine(driver=cls.driver,
                                        ip="127.0.0.1",
                                        port=8193,
                                        name="localhost")

    def test_machine_init(self):
        machine = Machine(driver=self.driver, ip="127.0.0.1")
        self.assertTrue(isinstance(machine, Machine))

    def test_machine_has_auto_name_from_ip(self):
        self.assertEqual(self.noNameMachine.ip, "127.0.0.1")
        self.assertEqual(self.noNameMachine.name, self.noNameMachine.ip)


@attr("integration")
class testFanuc30iDriverMachine(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        driver = Fanuc30iDriver("./lib/Fwlib32.dll",
                                extradlls=["./lib/fwlibe1.dll"])
        cls.fanuc30iMachine = Machine(driver=driver, ip=THREE_SIXTEEN)

    def test_fanuc30i_can_poll_hardware(self):
        self.fanuc30iMachine.createDatum()
        # if this doesn't raise an error then the machine responded

    def test_fanuc30i_can_reconnect_and_get_a_new_handle(self):
        oldHandle = self.fanuc30iMachine.handle
        self.fanuc30iMachine.reconnect()
        newHandle = self.fanuc30iMachine.handle
        self.assertNotEqual(oldHandle, newHandle)
