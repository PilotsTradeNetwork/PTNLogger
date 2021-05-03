# PTNLogger
Common logger package for use with PTN objects. 

The idea being that we can share the same logger, and this the same log formatting between our packages.  
The implementation contained within is relatively basic and does not allow much customisation, more flexibility can be 
added if it is required by various bot users.

## Functionality

Currently, the project offers the following accessor functions:

Create logger attaches a console and rotating file handler to your logger object by defualt. This is not changable 
today by design.

```python
def create_logger(name, log_directory=None, log_level=logging.DEBUG, backup_count=50):
    """
    Creates a logger with a console and rotating file handler attached to it.

    :param str name: The logger name
    :param str log_directory: The log directory to use, if None will use the current working directory + Logs
    :param logging log_level: The default log level to set. Defaults to logging.DEBUG,
        https://docs.python.org/3/library/logging.html#logging-levels
    :param int backup_count: How many files to keep, defaults to 50
    """
```

Get an existing logger you created, really you can just do ```python logging.getLogger(name)``` yourself, but we like 
making sure things are configured correctly.

```python
def get_logger(name):
    """
    Gets the logger with the associated name if it already exists. If the logger was not created before it will raise an 
    exception.
    
    :param str name: The logger name
    :returns: The logger object 
    :rtype: logging.Logger
    :raises PTNLoggerException: If the logger does not exist
    """
```

A directory cleanup function:

```python

def directory_cleanup(directory_list, backup_count=5):
    """
    Wrapper to cleanup a directory if needed.

    :param directory_list: A string or list of directories to cleanup
    :type directory_list: str or list.
    :param int backup_count: How many files to keep
    """
```

We also custom colour some prints in the console log based on the associated log level name for ease of reading.
