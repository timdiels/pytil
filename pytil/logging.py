# Copyright (C) 2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
#
# This file is part of pytil.
#
# pytil is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pytil is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pytil.  If not, see <http://www.gnu.org/licenses/>.

'''
Logging utilities.
'''

from contextlib import contextmanager
import logging

@contextmanager
def set_level(logger, level):
    '''
    Temporarily change log level of logger

    Parameters
    ----------
    logger : str or Logger
        Logger name
    level
        Log level to set

    Examples
    --------
    >>> with set_level('sqlalchemy.engine', logging.INFO):
    ...     pass # sqlalchemy log level is set to INFO in this block
    '''
    if isinstance(logger, str):
        logger = logging.getLogger(logger)
    original = logger.level
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(original)

def configure(log_file):
    '''
    Configure root logger to log INFO to stderr and DEBUG to log file.

    The log file is appended to. Stderr uses a terse format, while the log file
    uses a verbose unambiguous format.

    Root level is set to INFO.

    Parameters
    ----------
    log_file : Path
        File to log to

    Returns
    -------
    stderr_handler : logging.StreamHandler
        Handler that logs to stderr
    file_handler : logging.FileHandler
        Handler that logs to log_file
    '''
    # Note: do not use logging.basicConfig as it does not play along with caplog in testing
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # log info to stderr in terse format
    stderr_handler = logging.StreamHandler() # to stderr
    stderr_handler.setLevel(logging.INFO)
    stderr_handler.setFormatter(logging.Formatter('{levelname[0]}: {message}', style='{'))
    root_logger.addHandler(stderr_handler)

    # log debug to file in full format
    file_handler = logging.FileHandler(str(log_file))
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('{levelname[0]} {asctime} {name} ({module}:{lineno}):\n{message}\n', style='{'))
    root_logger.addHandler(file_handler)

    return stderr_handler, file_handler
