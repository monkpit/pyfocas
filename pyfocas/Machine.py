from pyfocas.Exceptions import FocasConnectionException
import logging
logging.basicConfig(level=logging.INFO)


class Machine(object):
    def __init__(self, driver, ip, port=8193, name=None):
        self.name = name if name is not None else ip
        self.ip = ip
        self.port = port
        self.driver = driver
        self.handle = self.driver.connect(ip, port)

    def createDatum(self):
        data = self.driver.poll(self.handle)
        data["machineName"] = self.name
        return data

    def reconnect(self):
        while True:
            try:
                self.handle = self.driver.reconnect(handle=self.handle,
                                                    ip=self.ip,
                                                    port=self.port)
                break
            except FocasConnectionException:
                logging.info("Reconnecting to machine: %s at %s"
                             % (self.name, self.ip))
