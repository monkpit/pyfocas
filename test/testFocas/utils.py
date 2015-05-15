import logging
import logging.handlers


class AssertingHandler(logging.handlers.BufferingHandler):

    def __init__(self, capacity):
        logging.handlers.BufferingHandler.__init__(self, capacity)

    def assert_logged(self, test_case, msg):
        for record in self.buffer:
            s = self.format(record)
            if s == msg:
                return
        test_case.assertTrue(False, "Failed to find log message: " + msg)
