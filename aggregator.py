import logging
import time

import pymongo

from pyfocas.Collector import Collector
from pyfocas.Machine import Machine
from FanucImplementation.DriverImplementations import Fanuc30iDriver
from pyfocas import Exceptions

THREE_SIXTEEN = "10.108.7.41"
THREE_TWENTY = "10.108.7.42"
FOUR_TWENTY_ONE = "10.108.7.39"
JAIME = "10.108.15.52"
THREE_EIGHTY_SEVEN = "10.108.7.12"
THREE_NINETY_SEVEN = "10.108.7.13"
THREE_NINETY_THREE = "10.108.7.14"
THREE_NINETY_SIX   = "10.108.7.15"

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
    driver30i = Fanuc30iDriver("./lib/Fwlib32.dll",
                               extradlls=["./lib/fwlibe1.dll"])

    machines = [Machine(driver=driver30i, ip=THREE_SIXTEEN, name="316"),
                Machine(driver=driver30i, ip=THREE_TWENTY, name="320"),
                Machine(driver=driver30i, ip=FOUR_TWENTY_ONE, name="421"),
                #Machine(driver=driver30i, ip=THREE_EIGHTY_SEVEN, name="387"),
                Machine(driver=driver30i, ip=THREE_NINETY_SEVEN, name="397"),
                Machine(driver=driver30i, ip=THREE_NINETY_SIX, name="396"),
                Machine(driver=driver30i, ip=THREE_NINETY_THREE, name="393"), ]
    collector = Collector(reporter=reporter, machines=machines)
    while True:
        collector.collect()
        time.sleep(.5)

if __name__ == "__main__":
    main()
