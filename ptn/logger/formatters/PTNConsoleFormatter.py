import copy
import sys
from enum import Enum

from .PTNCommonFormatter import PTNCommonFormatter


class Colours(Enum):
    """
    Some basic colours wraps the ANSI code for the colour object, see:
    https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
    """

    ERROR = '\033[91m'          #: Red
    WARNING = '\033[93m'        #: Yellow
    CRITICAL = '\033[95m'       #: Purples
    CLEAR = '\033[0m'           #: Clear the colour formatting


class PTNConsoleFormatter(PTNCommonFormatter):
    """
    Make things colourful by applying a colour onto the log level name. Only valid if you have a stdout.tty.
    """

    def format(self, record):
        # We use a copy or we impact any other log handlers that are using the record.
        formatted_record = copy.copy(record)
        if sys.stdout.isatty():
            try:
                formatted_record.levelname = Colours[record.levelname].value + record.levelname + Colours.CLEAR.value
            except KeyError:
                # Nothing defined for the log level name, just skip through.
                pass
        return super(PTNConsoleFormatter, self).format(formatted_record)
