# -*- coding: utf-8 -*-
""" Fwlib32_h.py

This file contains ctypes structures to match the data structures
found in the library header Fwlib32.h.

All classes contain `_pack_ = 4`; this comes from Fwlib32.h:
    #pragma pack(push,4)

Don't unit test these because it would basically be running tests against
the ctypes module itself and not any of our own code.

Further documentation can be found in the FOCAS documentation.
Look up the documentation of the Equivalent data type.
For example, for documentation on "AlarmStatus", look up "ODBALM".

"""

import ctypes

"""Constants"""

MAX_AXIS = 32
"""int: The maximum number of axes a control will return"""

ALL_AXES = -1
"""int: A constant value to request that a function return all axes at once"""


DATAIO_ALARM_MASK = (0x1 << 2) | (0x1 << 7)
SERVO_ALARM_MASK = 0x1 << 6
MACRO_ALARM_MASK = 0x1 << 8
OVERHEAT_ALARM_MASK = 0x1 << 5
OVERTRAVEL_ALARM_MASK = 0x1 << 4
SPINDLE_ALARM_MASK = 0x1 << 9
"""bit masks to determine alarm status
take an alarm data and AND it with the mask
If the result is True the alarm is active
If it's False it's cleared.

For example, see: DriverImplementations.alarmStringBuilder
"""


class AlarmStatus(ctypes.Structure):
    """
    Equivalent of ODBALM
    """
    _pack_ = 4
    _fields_ = [("dummy", ctypes.c_short * 2),
                ("data", ctypes.c_short), ]


ODBALM = AlarmStatus


class LoadElement(ctypes.Structure):
    """
    Equivalent of LOADELM
    """
    _pack_ = 4
    _fields_ = [("data", ctypes.c_long),
                ("decimal", ctypes.c_short),
                ("unit", ctypes.c_short),
                ("name", ctypes.c_char),
                ("suffix1", ctypes.c_char),
                ("suffix2", ctypes.c_char),
                ("reserve", ctypes.c_char), ]

LOADELM = LoadElement


class ServoLoad(ctypes.Structure):
    """
    Equivalent of ODBSVLOAD
    """
    _pack_ = 4
    _fields_ = [("load", LoadElement)]

ODBSVLOAD = ServoLoad


class SpindleLoad(ctypes.Structure):
    """
    Equivalent of ODBSPLOAD
    """
    _pack_ = 4
    _fields_ = [("load", LoadElement),
                ("speed", LoadElement), ]

ODBSPLOAD = SpindleLoad


class StatInfo(ctypes.Structure):
    _pack_ = 4
    _fields_ = [("hdck", ctypes.c_short),
                ("tmmode", ctypes.c_short),
                ("auto", ctypes.c_short),
                ("run", ctypes.c_short),
                ("motion", ctypes.c_short),
                ("mstb", ctypes.c_short),
                ("estop", ctypes.c_short),
                ("alarm", ctypes.c_short),
                ("edit", ctypes.c_short), ]

    @property
    def __dict__(self):
        # unreadable
        return dict((f, getattr(self, f)) for f, _ in self._fields_)


class ModalAux(ctypes.Structure):
    _pack_ = 4
    _fields_ = [("aux_data", ctypes.c_long),
                ("flag1", ctypes.c_char),
                ("flag2", ctypes.c_char), ]


class ModalAuxUnion(ctypes.Union):
    _pack_ = 4
    _fields_ = [("g_data", ctypes.c_char),
                ("g_rdata", ctypes.c_char * 35),
                ("g_1shot", ctypes.c_char * 4),
                ("aux", ModalAux),
                ("raux1", ModalAux * 27),
                ("raux2", ModalAux * MAX_AXIS), ]


class ModalData(ctypes.Structure):
    """
    Equivalent of ODBMDL
    """
    _pack_ = 4
    _fields_ = [("datano", ctypes.c_short),
                ("type", ctypes.c_short),
                ("modal", ModalAuxUnion), ]

ODBMDL = ModalData


class ExecutingProgram(ctypes.Structure):
    """
    Equivalent of ODBEXEPRG
    """
    _pack_ = 4
    _fields_ = [("name", ctypes.c_char * 36),
                ("oNumber", ctypes.c_long), ]

ODBEXEPRG = ExecutingProgram


class AxisName(ctypes.Structure):
    """
    Equivalent of ODBAXISNAME
    """
    _pack_ = 4
    _fields_ = [("name", ctypes.c_char),
                ("suffix", ctypes.c_char)]


ODBAXISNAME = AxisName


class AxisData(ctypes.Structure):
    """
    Equivalent of ODBAXDT
    """
    _pack_ = 4
    _fields_ = [("axisName", ctypes.c_char * 4),
                ("position", ctypes.c_long),
                ("decimalPosition", ctypes.c_short),
                ("unit", ctypes.c_short),
                ("flag", ctypes.c_short),
                ("_reserved", ctypes.c_short), ]


ODBAXDT = AxisData


class AlarmRecord(ctypes.Structure):
    _pack_ = 4
    _fields_ = [("recordType", ctypes.c_short),
                ("alarmGroup", ctypes.c_short),
                ("alarmNumber", ctypes.c_short),
                ("axis", ctypes.c_byte),
                ("_AlarmRecord_dummy", ctypes.c_byte)]


class MDIRecord(ctypes.Structure):
    _pack_ = 4
    _fields_ = [("recordType", ctypes.c_short),
                ("keycode", ctypes.c_byte),
                ("powerFlag", ctypes.c_byte),
                ("_MDIRecord_dummy", ctypes.c_char * 4), ]


class SignalRecord(ctypes.Structure):
    _pack_ = 4
    _fields_ = [("recordType", ctypes.c_short),
                ("signalName", ctypes.c_byte),
                ("oldSignal", ctypes.c_byte),
                ("newSignal", ctypes.c_byte),
                ("_SignalRecord_dummy", ctypes.c_byte),
                ("signalNumber", ctypes.c_short), ]


class DateOrPower(ctypes.Structure):
    _pack_ = 4
    _fields_ = [("recordType", ctypes.c_short),
                ("year", ctypes.c_byte),
                ("month", ctypes.c_byte),
                ("day", ctypes.c_byte),
                ("powerFlag", ctypes.c_byte),
                ("_DateOrPower_dummy", ctypes.c_byte * 2)]


class OperationHistoryDataUnion(ctypes.Union):
    """
    Union for operation history data
    """
    _pack_ = 4
    _fields_ = [("alarm", AlarmRecord),
                ("mdi", MDIRecord),
                ("signal", SignalRecord),
                ("dateOrPower", DateOrPower), ]


class OperationHistory(ctypes.Structure):
    """
    Equivalent of ODBHIS
    """
    _pack_ = 4
    _fields_ = [("startNumber", ctypes.c_ushort),
                ("_ODBHIS_type", ctypes.c_short),
                ("endNumber", ctypes.c_ushort),
                ("data", OperationHistoryDataUnion * 10)]


ODBHIS = OperationHistory


class ProgramDirectory2(ctypes.Structure):
    """
    Equivalent of PRGDIR2
    """
    _pack_ = 4
    _fields_ = [("number", ctypes.c_short),
                ("length", ctypes.c_long),
                ("comment", ctypes.c_char * 51),
                ("_ProgramDirectory2_dummy", ctypes.c_char), ]

PRGDIR2 = ProgramDirectory2


class PanelSignals150(ctypes.Structure):
    """
    Equivalent of IODBSGNL with less data
    """
    _pack_ = 4
    _fields_ = [("_PanelSignals150_dummy", ctypes.c_short),  # dummy
                ("type", ctypes.c_short),  # data select flag 
                ("mode", ctypes.c_short),  # mode signal 
                ("manualFeedAxis", ctypes.c_short),  # Manual handle feed axis selection signal 
                ("manualFeedDistance", ctypes.c_short),  # Manual handle feed travel distance selection signal 
                ("rapidOverride", ctypes.c_short),  # rapid traverse override signal 
                ("jogOverride", ctypes.c_short),  # manual feedrate override signal 
                ("feedOverride", ctypes.c_short),  # feedrate override signal 
                ("spindleOverride", ctypes.c_short),  # (not used) 
                ("blockDelete", ctypes.c_short),  # optional block skip signal 
                ("singleBlock", ctypes.c_short),  # single block signal 
                ("machineLock", ctypes.c_short),  # machine lock signal 
                ("dryRun", ctypes.c_short),  # dry run signal 
                ("memoryProtection", ctypes.c_short),  # memory protection signal 
                ("feedHold", ctypes.c_short),  # automatic operation halt signal 
                ("manualRapid", ctypes.c_short),  # (not used)
                ("_PanelSignals150_dummy2", ctypes.c_short * 2), ] # dummy


class PanelSignals160(ctypes.Structure):
    """
    Equivalent of IODBSGNL
    """
    _pack_ = 4
    _fields_ = [("_PanelSignals160_dummy", ctypes.c_short),  # dummy 
                ("type", ctypes.c_short),  # data select flag 
                ("mode", ctypes.c_short),  # mode signal 
                ("manualFeedAxis", ctypes.c_short),  # Manual handle feed axis selection signal 
                ("manualFeedDistance", ctypes.c_short),  # Manual handle feed travel distance selection signal 
                ("rapidOverride", ctypes.c_short),  # rapid traverse override signal 
                ("jogOverride", ctypes.c_short),  # manual feedrate override signal 
                ("feedOverride", ctypes.c_short),  # feedrate override signal 
                ("spindleOverride", ctypes.c_short),  # (not used) 
                ("blockDelete", ctypes.c_short),  # optional block skip signal 
                ("singleBlock", ctypes.c_short),  # single block signal 
                ("machineLock", ctypes.c_short),  # machine lock signal 
                ("dryRun", ctypes.c_short),  # dry run signal 
                ("memoryProtection", ctypes.c_short),  # memory protection signal 
                ("feedHold", ctypes.c_short),]  # automatic operation halt signal 

IODBSGNL = PanelSignals160


class PMCData(ctypes.Structure):
    """
    Actual PMC values that were read
    Used to replace anonymous struct in IODBPMC called "u"
    """
    _pack_ = 1
    _fields_ = [("cdata", ctypes.c_byte * 5),
                ("idata", ctypes.c_short * 5),
                ("ldata", ctypes.c_byte * 5), ]

    @property
    def pmcValue(self):
        if self.cdata[0] < 0:
            self.cdata[0] = -self.cdata[0] - 1
        return self.cdata[0]


class PMC(ctypes.Structure):
    """
    A data structure to hold values read from PMC addresses
    Equivalent of IODBPMC
    """
    _pack_ = 4
    _fields_ = [("addressType", ctypes.c_short),
                ("dataType", ctypes.c_short),
                ("startAddress", ctypes.c_short),
                ("endAddress", ctypes.c_short),
                ("data", PMCData), ]

IODBPMC = PMC


class FAxis(ctypes.Structure):
    _pack_ = 4
    _fields_ = [("_absolute", ctypes.c_long * MAX_AXIS),
                ("_machine", ctypes.c_long * MAX_AXIS),
                ("_relative", ctypes.c_long * MAX_AXIS),
                ("_distance", ctypes.c_long * MAX_AXIS), ]

    @property
    def __dict__(self):
        # unreadable
        return dict((f, [x for x in getattr(self, f)])
                    for (f, _) in self._fields_)
        # return {"absolute": self.absolute,
        #        "machine": self.machine,
        #        "relative": self.relative,
        #        "distance": self.distance}


class OAxis(ctypes.Structure):
    _pack_ = 4
    _fields_ = [("absolute", ctypes.c_long),
                ("machine", ctypes.c_long),
                ("relative", ctypes.c_long),
                ("distance", ctypes.c_long), ]

    @property
    def __dict__(self):
        # unreadable
        return dict((f, getattr(self, f)) for f, _ in self._fields_)


class PositionUnion(ctypes.Union):
    """
    Alias for the anonymous union "pos" defined in some fwlib32 structures
    """
    _pack_ = 4
    _fields_ = [("_faxis", FAxis),
                ("_oaxis", OAxis), ]

    @property
    def __dict__(self):
        # unreadable
        return dict([("faxis", self._faxis.__dict__),
                    ("oaxis", self._oaxis.__dict__)])


class DynamicResult(ctypes.Structure):
    """
    Alias for ODBDY2 because what does that even mean
    """
    _pack_ = 4
    _fields_ = [("_DynamicResult_dummy", ctypes.c_short),
                ("axis", ctypes.c_short),
                ("alarm", ctypes.c_long),
                ("programNumber", ctypes.c_long),
                ("mainProgramNumber", ctypes.c_long),
                ("sequenceNumber", ctypes.c_long),
                ("actualFeed", ctypes.c_long),
                ("actualSpindleSpeed", ctypes.c_long),
                ("position", PositionUnion), ]

    @property
    def __dict__(self):
        # unreadable
        return dict((f, getattr(self, f)) for f, _ in self._fields_)

ODBDY2 = DynamicResult


class IDBPMMGTI(ctypes.Structure):
    """
    Equivalent of IDBPMMGTI in FOCAS documentation
    """
    _pack_ = 4
    _fields_ = [("top", ctypes.c_long),
                ("num", ctypes.c_long), ]


class ODBPMMGET(ctypes.Structure):
    """
    Equivalent of ODBPMMGET in FOCAS documentation
    """
    _pack_ = 4
    _fields_ = [("position", ctypes.c_long),
                ("actualFeed", ctypes.c_long),
                ("data", ctypes.c_long * 20),
                ("number", ctypes.c_long * 20),
                ("axis", ctypes.c_short * 20),
                ("type", ctypes.c_short * 20),
                ("alarmAxis", ctypes.c_char * 40),
                ("alarmNumber", ctypes.c_ushort * 40),
                ("channel", ctypes.c_long),
                ("group", ctypes.c_long), ]


class ProgramData(ctypes.Structure):
    """
    Equivalent of ODBPRO
    """
    _pack_ = 4
    _fields_ = [("dummy", ctypes.c_short * 2),
                ("program", ctypes.c_long),
                ("mainProgram", ctypes.c_long)]


ODBPRO = ProgramData
