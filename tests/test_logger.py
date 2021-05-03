import inspect
import logging
import shutil
import tempfile

import mock
import pytest

from ptn.logger.handlers.TimedPatternFileHandler import TimedPatternFileHandler
from ptn.logger.ptnlogger import create_logger, get_logger, PTNLoggerException


def test_create_logger():
    logger = create_logger(inspect.currentframe().f_code.co_name)
    assert logger.name == inspect.currentframe().f_code.co_name
    assert len(logger.handlers) == 2


def test_create_logger_with_level():
    logger = create_logger(inspect.currentframe().f_code.co_name, log_level=logging.ERROR)
    assert logger.name == inspect.currentframe().f_code.co_name
    assert len(logger.handlers) == 2

    assert logger.level == logging.ERROR
    for handler in list(logger.handlers):
        print(handler.name)
        assert handler.level == logging.ERROR


def test_create_logger_custom_folder():
    folder = tempfile.mkdtemp()
    logger = create_logger(inspect.currentframe().f_code.co_name, log_directory=folder)
    assert logger.name == inspect.currentframe().f_code.co_name
    assert len(logger.handlers) == 2
    for log_handler in list(logger.handlers):
        if isinstance(log_handler, TimedPatternFileHandler):
            # Check the folder name is the file name, meaning we are in the right directory
            assert folder in log_handler.filename
    try:
        shutil.rmtree(folder)
    except OSError:
        pass


def test_get_existing_logger():
    initial_logger = create_logger(inspect.currentframe().f_code.co_name)
    second_logger = get_logger(inspect.currentframe().f_code.co_name)
    # make sure we get the same thing back
    assert initial_logger == second_logger


def test_get_existing_logger_fails():
    with pytest.raises(PTNLoggerException):
        get_logger(inspect.currentframe().f_code.co_name)


@mock.patch('ptn.logger.ptnlogger.sys.stdout')
def test_console_tty(mocktty, caplog):
    mocktty.isatty.return_value = True
    caplog.clear()
    logger = create_logger(inspect.currentframe().f_code.co_name)
    logger.propagate = True     # needed for Caplog
    logger.info('Info message')
    for record in caplog.records:
        assert record.levelname == 'INFO'
    assert 'Info message' in caplog.text


def test_call_logger_twice():
    logger = create_logger(inspect.currentframe().f_code.co_name)
    assert logger.name == inspect.currentframe().f_code.co_name
    assert len(logger.handlers) == 2

    # Recreate it again, it should not re-add
    logger = create_logger(inspect.currentframe().f_code.co_name)
    assert logger.name == inspect.currentframe().f_code.co_name
    assert len(logger.handlers) == 2


def test_log_level_info(caplog):
    caplog.clear()
    logger = create_logger(inspect.currentframe().f_code.co_name)
    # Caplog needs to propagate the log messages so it gets them
    logger.propagate = True
    logger.info('This is an info message')
    for record in caplog.records:
        assert record.levelname == 'INFO'
    assert 'This is an info message' in caplog.text


def test_log_level_debug(caplog):
    caplog.clear()
    logger = create_logger(inspect.currentframe().f_code.co_name)
    # Caplog needs to propagate the log messages so it gets them
    logger.propagate = True
    logger.debug('This is a debug message')
    for record in caplog.records:
        assert record.levelname == 'DEBUG'
    assert 'This is a debug message' in caplog.text


def test_log_level_critical(caplog):
    caplog.clear()
    logger = create_logger(inspect.currentframe().f_code.co_name)
    # Caplog needs to propagate the log messages so it gets them
    logger.propagate = True
    logger.critical('This is a critical message')
    for record in caplog.records:
        assert record.levelname == 'CRITICAL'
    assert 'This is a critical message' in caplog.text


def test_log_level_error(caplog):
    caplog.clear()
    logger = create_logger(inspect.currentframe().f_code.co_name)
    # Caplog needs to propagate the log messages so it gets them
    logger.propagate = True
    logger.error('This is an error message')
    for record in caplog.records:
        assert record.levelname == 'ERROR'
    assert 'This is an error message' in caplog.text
