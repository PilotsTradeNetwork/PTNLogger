import logging
import os
import sys

from .foldercleanup.TimedDirectoryCleanup import TimedDirectoryCleanup
from .formatters.PTNCommonFormatter import PTNCommonFormatter
from .formatters.PTNConsoleFormatter import PTNConsoleFormatter
from .handlers.TimedPatternFileHandler import TimedPatternFileHandler


def get_logger(name):
    logger = logging.getLogger(name)
    if len(logger.handlers) == 0:
        # No handlers attached, means the logger was not created before, means you done goofed up.
        raise EnvironmentError('You should call create_logger first to configure your log handlers.')
    return logger


def _check_handler_exists(find_handler, logger):
    """
    Check whether we already have a handler with the associated type on the logger, we don't want to double things up
    """
    for existing_handler in list(logger.handlers):
        handler_streamname = getattr(find_handler.stream, 'name', str(find_handler.stream))
        existing_handler_streamname = getattr(existing_handler.stream, 'name', str(existing_handler.stream))

        if handler_streamname != existing_handler_streamname:
            # Did not match, move on
            continue
        # We have a handler with this name, return the state
        return True
    return False


def directory_cleanup(directory_list, backup_count=5):
    """
    Wrapper to cleanup a directory if needed.

    :param directory_list: A string or list of directories to cleanup
    :type directory_list: str or list.
    :param int backup_count: How many files to keep
    """
    if isinstance(directory_list, str):
        directory_list = [directory_list]

    for directory in directory_list:
        if os.path.isabs(directory):
            path = directory
        else:
            path = os.path.join(os.getcwd(), directory)

        if not os.path.exists(path):
            # Make it if needed
            os.makedirs(path)

        TimedDirectoryCleanup(directory=directory, backup_count=backup_count).cleanup()


def create_logger(name, log_directory=None, loglevel=logging.DEBUG, backup_count=50):
    """
    Creates a logger with a console and rotating file handler attached to it.

    :param str name: The logger name
    :param str log_directory: The log directory to use, if None will use the current working directory + Logs
    :param logging.level loglevel: The default log level to set. Defaults to logging.DEBUG
    :param int backup_count: How many files to keep, defaults to 50
    """
    # Gets a logger that has a console and rotating file logger attached to it

    logger = logging.getLogger(name)
    logger.setLevel(loglevel)

    # Do we want to propagate log messages, maybe not?
    logger.propagate = False

    # Go add a console handler to the logger
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(PTNConsoleFormatter())
    handler.setLevel(loglevel)

    if not _check_handler_exists(handler, logger):
        logger.addHandler(handler)

    if not log_directory:
        # Try to generate a default directory in the working directory /logs. Make it if needed
        log_directory = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(log_directory):
            os.mkdir(log_directory)

    # Now the rotating file logger to write to the file system
    pattern = '%Y-%m-%d_%H-%M-%S'
    filename = os.path.join(log_directory, f'{name}_{pattern}.log')
    rotating_file_handler = TimedPatternFileHandler(
        filename,
        mode='a',
        backup_count=backup_count
    )
    rotating_file_handler.setFormatter(PTNCommonFormatter())
    rotating_file_handler.setLevel(loglevel)
    handler.setLevel(loglevel)

    if not _check_handler_exists(rotating_file_handler, logger):
        logger.addHandler(rotating_file_handler)

    return logger
