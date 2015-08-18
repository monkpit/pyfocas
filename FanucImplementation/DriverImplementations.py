from ctypes import *

from pyfocas.Driver import FocasDriverBase
from pyfocas.Exceptions import FocasExceptionRaiser
from Fwlib32_h import *

AUTO_LABELS = ["MDI", "AUTO", "AUTO", "EDIT", "AUTO", "MANUAL", "MANUAL"]
RUN_LABELS = ["STOPPED", "READY (WAITING)", "FEED HOLD", "ACTIVE", "ACTIVE"]

gBlockString = ""


class Fanuc30iDriver(FocasDriverBase):
    ip = ""
    port = 0
    timeout = 0

    def connect(self, ip, port, timeout=10):
        func = self.dll.cnc_allclibhndl3
        func.restype = c_short
        handle = c_ushort(0)
        result = func(ip, port, timeout, byref(handle))
        FocasExceptionRaiser(result, context=self)
        self.ip = ip
        self.port = port
        self.timeout = timeout
        return handle

    def disconnect(self, handle):
        self.dll.cnc_freelibhndl(handle)

    def registerPollMethods(self):
        # there has GOT to be a way to do this with a decorator
        self.addPollMethod(self.getProgramName)
        self.addPollMethod(self.getBlockNumber)
        self.addPollMethod(self.getActiveTool)
        self.addPollMethod(self.getControlStatus)
        self.addPollMethod(self.getPMCValues)
        self.addPollMethod(self.getServoAndAxisLoads)
        self.addPollMethod(self.getAlarmStatus)
        self.addPollMethod(self.getCurrentBlock)

    def getProgramName(self, handle):
        func = self.dll.cnc_exeprgname
        func.restype = c_short
        executingProgram = ExecutingProgram()
        result = func(handle, byref(executingProgram))
        FocasExceptionRaiser(result, context=self)
        data = {}
        data["programName"] = executingProgram.name
        data["oNumber"] = executingProgram.oNumber
        return data

    def getBlockNumber(self, handle):
        dynamic = DynamicResult()
        func = self.dll.cnc_rddynamic2
        func.restype = c_short
        result = func(handle,
                      -1,
                      sizeof(DynamicResult),
                      byref(dynamic))
        FocasExceptionRaiser(result, context=self)
        data = {}
        data["blockNumber"] = dynamic.sequenceNumber
        return data

    def getActiveTool(self, handle):
        func = self.dll.cnc_modal
        func.restype = c_short
        modalData = ModalData()
        result = func(handle, 108, 1, byref(modalData))
        FocasExceptionRaiser(result, context=self)
        data = {}
        data["activeTool"] = modalData.modal.aux.aux_data
        return data

    def getControlStatus(self, handle):
        func = self.dll.cnc_statinfo
        func.restype = c_short
        statInfo = StatInfo()
        result = func(handle, byref(statInfo))
        FocasExceptionRaiser(result, context=self)
        data = {}
        try:
            data["autoMode"] = AUTO_LABELS[statInfo.auto]
        except IndexError:
            data["autoMode"] = statInfo.auto

        try:
            data["runStatus"] = RUN_LABELS[statInfo.run]
        except IndexError:
            data["runStatus"] = statInfo.run

        data["isEditing"] = bool(statInfo.edit)
        return data

    def getPMCValues(self, handle):
        """
        Checks the PMC addresses and returns
        their values from the control.
        """
        """ getPMCfunc is the ctypes function imported
            from the dll.                          """
        getPMCfunc = self.dll.pmc_rdpmcrng
        getPMCfunc.restype = c_short
        """ length = 9 is a hardcoded value from the
            vendor's documentation.                """
        length = 9
        pmcAddresses = {"Fovr": 12,
                        "Sovr": 30}
        data = {}
        for pmcName in pmcAddresses:
            pmcAddress = pmcAddresses[pmcName]
            pmcdata = PMC()
            result = getPMCfunc(handle,
                                0,
                                0,
                                pmcAddress,
                                pmcAddress,
                                length,
                                byref(pmcdata))
            FocasExceptionRaiser(result, context=self)
            data[pmcName] = pmcdata.data.pmcValue
        return data

    def getServoAndAxisLoads(self, handle):
        getServoLoadFunc = self.dll.cnc_rdspmeter
        getServoLoadFunc.restype = c_short
        num = c_short(MAX_AXIS)
        loads = (SpindleLoad * MAX_AXIS)()
        result = getServoLoadFunc(handle, 0, byref(num), loads)
        FocasExceptionRaiser(result, context=self)
        # lambda to calculate the actual spindle load value
        spload = lambda s: s.load.data / pow( 10.0, s.load.decimal)
        loads = {s.load.name : spload(s) for s in loads if s.load.name is not "\x00" }
        # TODO: add in axis loads
        getAxisLoadFunc = self.dll.cnc_rdsvmeter
        getAxisLoadFunc.restype = c_short
        axloads = (ServoLoad * MAX_AXIS)()
        num = c_short(MAX_AXIS)
        result = getAxisLoadFunc(handle, byref(num), axloads)
        FocasExceptionRaiser(result, context=self)
        axloads = {s.load.name : spload(s) for s in axloads if s.load.name is not "\x00"}
        loads.update(axloads)
        data = {'loads': loads}
        return data

    def getAlarmStatus(self, handle):
        getAlarmStatusFunc = self.dll.cnc_alarm
        getAlarmStatusFunc.restype = c_short
        alarm_data = AlarmStatus()
        result = getAlarmStatusFunc(handle, byref(alarm_data))
        FocasExceptionRaiser(result, context=self)
        alarm_data = alarm_data.data
        data = {}
        data["alarm"] = alarmStringBuilder(alarm_data=alarm_data)
        return data

    def getCurrentBlock(self, handle):
        global gBlockString
        getCurrentBlockFunc = self.dll.cnc_rdexecprog
        getCurrentBlockFunc.restype = c_short
        blockstring = (c_char * 255)()
        blocklength = c_ushort(255)
        blocknumber = c_short(0)
        result = getCurrentBlockFunc(handle, byref(blocklength),
                                     byref(blocknumber), blockstring)
        FocasExceptionRaiser(result, context=self)
        data = {}
        if blockstring.value is not gBlockString:
            data["currentBlock"] = blockstring.value
            gBlockString = blockstring.value

        return data


def alarmStringBuilder(alarm_data):
    alarms = []
    if alarm_data & DATAIO_ALARM_MASK:
        alarms.append("DATAIO")
    if alarm_data & SERVO_ALARM_MASK:
        alarms.append("SERVO")
    if alarm_data & MACRO_ALARM_MASK:
        alarms.append("MACRO")
    if alarm_data & OVERHEAT_ALARM_MASK:
        alarms.append("OVERHEAT")
    if alarm_data & OVERTRAVEL_ALARM_MASK:
        alarms.append("OVERTRAVEL")
    if alarm_data & SPINDLE_ALARM_MASK:
        alarms.append("SPINDLE")

    return alarms
