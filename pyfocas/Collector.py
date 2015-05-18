from __future__ import print_function


class Collector(object):
    def __init__(self, reporter, machines):
        self.machines = machines
        # a reporter is a function that takes a single machine as input
        self.reporter = reporter

    # untestable
    def collect(self):
        # apply the reporter function to each machine in the list
        return [x for x in map(self.reporter, self.machines) if x is not None]
