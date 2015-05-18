from __future__ import print_function
import unittest
from nose.tools import raises, assert_raises
from pyfocas import Exceptions
from itertools import chain


class testFocasExceptions(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        pass

    @raises(Exceptions.FocasConnectionException)
    def test_FocasExceptionRaiser_raises_FocasConnectionException(self):
        Exceptions.FocasExceptionRaiser(-16)

    @raises(Exceptions.FocasAlarmException)
    def test_FocasExceptionRaiser_raises_FocasAlarmException(self):
        Exceptions.FocasExceptionRaiser(15)

    @raises(Exceptions.FocasOtherException)
    def test_FocasExceptionRaiser_raises_FocasOtherException(self):
        Exceptions.FocasExceptionRaiser(1)

    def test_all_Exceptions_subclass_FocasException(self):
        # check that all class members of the Exceptions module
        # are subclasses of Exceptions.FocasException
        import inspect

        def isFocasExceptionSubclass(klass=None):
            return issubclass(klass, Exceptions.FocasException)

        exceptionClasses = [klass for (_, klass) in inspect.getmembers(Exceptions) if inspect.isclass(klass)]
        truthArray = map(isFocasExceptionSubclass, exceptionClasses)
        self.assertTrue(all(truthArray))

    def test_valid_nonzero_exception_values_raise_FocasExceptions(self):
        negative_value_set_1 = xrange(-1, -12, -1)
        negative_value_set_2 = xrange(-15, -18, -1)

        positive_value_set_1 = xrange(1, 20)

        for x in chain(negative_value_set_1,
                       negative_value_set_2,
                       positive_value_set_1):

                            assert_raises(Exceptions.FocasException,
                                          Exceptions.FocasExceptionRaiser,
                                          x)

    def test_zero_exception_value_does_not_raise_any_exception(self):
        try:
            status_ok_value = 0
            Exceptions.FocasExceptionRaiser(status_ok_value)
            # pass if no exception was raised
        except:
            self.fail()

    @raises(Exception)
    def test_value_out_of_range_generates_regular_Exception(self):
        invalid_error_value = 999
        Exceptions.FocasExceptionRaiser(invalid_error_value)
