#!/usr/bin/env python

import logging
import time

import pymongo

from pyfocas.Collector import Collector
from pyfocas.Machine import Machine
from FanucImplementation.DriverImplementations import Fanuc30iDriver
from pyfocas import Exceptions

THREE_SIXTEEN = "10.108.7.41"
THREE_TWENTY = "10.108.7.42"
THREE_TWENTY_TWO = "10.108.7.44"
THREE_TWENTY_SIX = "10.108.7.45"
FOUR_SIXTEEN = "10.108.7.46"
FOUR_EIGHTEEN = "10.108.7.47"
FOUR_TWENTY_ONE = "10.108.7.39"
JAIME = "10.108.15.52"
THREE_EIGHTY_SEVEN = "10.108.7.12"
THREE_NINETY_SEVEN = "10.108.7.13"
THREE_NINETY_THREE = "10.108.7.14"
THREE_NINETY_SIX   = "10.108.7.15"



def logging_reporter(machine):
    """
    The logging_reporter is a reporter function to be passed
    into a Collector object.
    logging_reporter is intended for debugging purposes,
    all machine datums will be logged to the default logger.

    Parameters: Machine machine

                The reporter expects to be passed a
                Machine object that it will report on.

    Return value: dict data
                The reporter will return a dictionary
                with key:value pairs representing the
                data handled by the reporter.
    """
    try:
        data = machine.createDatum()
        logging.info(data)
        return data
    except Exceptions.FocasConnectionException:
        machine.reconnect()


def mongo_reporter(collection, machine):
    """
    The logging_reporter is a reporter function to be passed
    into a Collector object.
    logging_reporter is intended for debugging purposes,
    all machine datums will be logged to the default logger.

    Parameters: Machine machine

                The reporter expects to be passed a
                Machine object that it will report on.

    Return value: dict data
                The reporter will return a dictionary
                with key:value pairs representing the
                data handled by the reporter.
    """
    try:
        data = machine.createDatum()
        collection.insert_one(data)
        return data
    except Exceptions.FocasConnectionException:
        machine.reconnect()


def main():
    """
    The main method of the program. Runs a Collector forever.
    """

    """ Setup logging """
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Starting Collector")

    """ Setup MongoDB logging client """
    client = pymongo.MongoClient("mongodb://srvhoursapp25.nov.com:27017/")
    db = client['test']
    collection = db['focas']

    def reporter(machine):
        return mongo_reporter(collection, machine)

    """ Instantiate Fanuc30iDriver """
    driver30i = Fanuc30iDriver("./lib/Fwlib32.dll",
                               extradlls=["./lib/fwlibe1.dll"])

    """ List of Machine objects to initialize the Collector with """
    machines = [Machine(driver=driver30i, ip=THREE_SIXTEEN, name="316"),
                Machine(driver=driver30i, ip=THREE_TWENTY, name="320"),
                #Machine(driver=driver30i, ip=THREE_TWENTY_TWO, name="322"),
                #Machine(driver=driver30i, ip=THREE_TWENTY_SIX, name="326"),
                #Machine(driver=driver30i, ip=FOUR_SIXTEEN, name="416"),
                #Machine(driver=driver30i, ip=FOUR_EIGHTEEN, name="418"),
                Machine(driver=driver30i, ip=FOUR_TWENTY_ONE, name="421"),
                #Machine(driver=driver30i, ip=THREE_EIGHTY_SEVEN, name="387"),
                Machine(driver=driver30i, ip=THREE_NINETY_SEVEN, name="397"),
                Machine(driver=driver30i, ip=THREE_NINETY_SIX, name="396"),
                Machine(driver=driver30i, ip=THREE_NINETY_THREE, name="393"), ]
    """ Create the Collector """
    collector = Collector(reporter=reporter, machines=machines)

    while True:
        """ Run the collector until the process is interrupted """
        collector.collect()
        time.sleep(.5)

if __name__ == "__main__":
    main()
