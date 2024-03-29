import logging
logger = logging.getLogger(__name__)

class GPIO:
    BOARD = "board"
    BCM = "broadcom"
    OUT = "out"
    IN = "in"
    PUD_DOWN = "pudDown"
    PUD_UP = "pudUp"
    HIGH = True
    LOW = False

    _pins = {}

    def __init__(self):
        pass

    @classmethod
    def setup(self, param1, param2, pull_up_down=True):
        self._pins[param1] = param2

    @classmethod
    def output(self, param1, param2):
        pass

    @classmethod
    def setwarnings(self, param1):
        pass

    @classmethod
    def setmode(self, param1):
        logging.debug("Using debug RPI.GPIO")
        # pass

    @classmethod
    def cleanup(self):
        pass

    @classmethod
    def input(self, param1) -> bool:
        return self._pins[param1]
