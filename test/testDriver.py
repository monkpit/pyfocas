from __future__ import print_function
import unittest
from nose.tools import raises
from nose.plugins.attrib import attr
from pyfocas.Driver import ExampleDriver, FocasDriverBase
from FanucImplementation.DriverImplementations import Fanuc30iDriver
import ctypes


class TestDriverWithNoPollMethods(FocasDriverBase):
    def connect(self, ip, port):
        pass

    def disconnect(self, handle):
        pass

    def reconnect(self, ip, port):
        pass

    def registerPollMethods(self):
        pass


class BadPollDriver(FocasDriverBase):
    def connect(self, ip, port):
        pass

    def disconnect(self, handle):
        pass

    def reconnect(self, ip, port):
        pass

    def registerPollMethods(self):
        self.addPollMethod("deadbeef")


class testFocasDriverBase(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        cls.ExampleDriver = ExampleDriver("./lib/Fwlib32.dll",
                                          extradlls=["./lib/fwlibe1.dll"])
        cls.NoPollDriver = \
            TestDriverWithNoPollMethods("./lib/Fwlib32.dll",
                                        extradlls=["./lib/fwlibe1.dll"])

    def test_Driver_loads_correctly(self):
        self.assertTrue(isinstance(self.ExampleDriver.dll, ctypes.WinDLL))

    @raises(TypeError)
    def test_instantiating_FocasDriverBase_raises_TypeError(self):
        FocasDriverBase("./lib/Fwlib32.dll")

    def test_Driver_with_no_poll_methods_returns_error_message(self):
        self.NoPollDriver.poll()["error"]
        # if this does not raise an exception then the test should pass

    @raises(NameError)
    def test_Driver_with_non_callable_poll_methods_raises_NameError(self):
        BadPollDriver("./lib/Fwlib32.dll", extradlls=["./lib/fwlibe1.dll"])
