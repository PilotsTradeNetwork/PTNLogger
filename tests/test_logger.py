import inspect
import logging

import mock
import pytest

from ptn.logger.logging import create_logger, get_logger


def test_create_logger():
    logger = create_logger(inspect.currentframe().f_code.co_name)
    assert logger.name == inspect.currentframe().f_code.co_name
    assert len(logger.handlers) == 2


def test_create_logger_with_level():
    logger = create_logger(inspect.currentframe().f_code.co_name, loglevel=logging.ERROR)
    assert logger.name == inspect.currentframe().f_code.co_name
    assert len(logger.handlers) == 2

    assert logger.level == logging.ERROR
    for handler in list(logger.handlers):
        print(handler.name)
        assert handler.level == logging.ERROR


def test_create_logger_custom_folder():
    # TODO:
    pass


def test_get_existing_logger():
    initial_logger = create_logger(inspect.currentframe().f_code.co_name)
    second_logger = get_logger(inspect.currentframe().f_code.co_name)
    # make sure we get the same thing back
    assert initial_logger == second_logger


def test_get_existing_logger_fails():
    with pytest.raises(EnvironmentError):
        get_logger(inspect.currentframe().f_code.co_name)


@mock.patch('ptn.logger.logging.sys.stdout')
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
