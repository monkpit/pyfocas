import logging
import time

import pymongo

from Focas.Collector import Collector
from Focas.Machine import Machine
from FanucImplementation.DriverImplementations import Fanuc30iDriver
from Focas import Exceptions

THREE_SIXTEEN = "10.108.7.41"
THREE_TWENTY = "10.108.7.42"

collection = None


def logging_reporter(machine):
    try:
        data = machine.createDatum()
        logging.info(data)
        return data
    except Exceptions.FocasConnectionException:
        machine.reconnect()


def mongo_reporter(machine):
    try:
        data = machine.createDatum()
        collection.insert_one(data)
        return data
    except Exceptions.FocasConnectionException:
        machine.reconnect()


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Starting Collector")

    client = pymongo.MongoClient("mongodb://srvhoursapp25.nov.com:27017/")
    db = client['test']
    global collection
    collection = db['focas']

    reporter = mongo_reporter
    driver = Fanuc30iDriver("./lib/Fwlib32.dll",
                            extradlls=["./lib/fwlibe1.dll"])
    machines = [Machine(driver=driver, ip=THREE_SIXTEEN, name="316"),
                Machine(driver=driver, ip=THREE_TWENTY, name="320")]
    collector = Collector(reporter=reporter, machines=machines)
    while True:
        collector.collect()
        time.sleep(.5)

if __name__ == "__main__":
    main()
