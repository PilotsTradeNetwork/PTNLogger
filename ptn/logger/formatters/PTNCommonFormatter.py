import logging

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class PTNCommonFormatter(logging.Formatter):

    def __init__(self, fmt=LOG_FORMAT, datefmt=None):
        """
        A common log formatting object for log objects to use.

        :param str fmt: The log format as a string. Can be altered but defaults to:
            '%(ascitime)s = %(name)s - %(levelname)s - %(message)s'
        :param str datefmt: The date format string to use, default None.
        """
        super(PTNCommonFormatter, self).__init__(fmt, datefmt)
