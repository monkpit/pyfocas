import os
import sys
import ctypes
from ctypes.util import find_library
from abc import ABCMeta, abstractmethod
from datetime import datetime


class FocasDriverBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, filename, extradlls=[], timeout=10):
        self.timeout = timeout
        self.extradlls = []
        for extradll in extradlls:
            extradll = find_library(extradll)
            self.extradlls.append(ctypes.windll.LoadLibrary(extradll))

        dllfile = find_library(filename)
        self.dll = ctypes.windll.LoadLibrary(dllfile)

        self._poll_methods = []
        self.registerPollMethods()

    @abstractmethod
    def registerPollMethods(self):
        # every pollmethod should return a dictionary containing your data
        pass  # pragma: no cover

    @abstractmethod
    def connect(self, ip, port):
        pass  # pragma: no cover

    def reconnect(self, handle, ip, port):
        self.disconnect(handle)
        return self.connect(ip, port)

    @abstractmethod
    def disconnect(self, handle):
        pass  # pragma: no cover

    def addPollMethod(self, method):
        if callable(method):
            self._poll_methods.append(method)
        else:
            raise NameError("addPollMethod: %s was not callable" % method)

    def poll(self, handle=None):
        # initialize the data object with a timestamp
        data = {"timestamp": datetime.now()}
        if handle is not None and self._poll_methods != []:
            for poll_method in self._poll_methods:
                poll_reading = poll_method(handle)
                if isinstance(poll_reading, dict):
                    data.update(poll_reading)
        else:
            data.update({"error":
                         "%s has no _poll_methods!" % self.__class__.__name__})
        return data


class ExampleDriver(FocasDriverBase):
    # errors should raise a subclass of FocasException
    def connect(self, ip, port):
        pass  # pragma: no cover

    def disconnect(self, handle):
        pass  # pragma: no cover

    def registerPollMethods(self):
        self.addPollMethod(self.test)
        self.addPollMethod(self.test2)

    def test(self):
        return {"test_driver_key": "test_driver_value"}

    def test2(self):
        return {"test_driver_key2": "test_driver_value2"}
