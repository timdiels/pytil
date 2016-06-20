# Copyright (C) 2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
# 
# This file is part of Chicken Turtle Util.
# 
# Chicken Turtle Util is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Chicken Turtle Util is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with Chicken Turtle Util.  If not, see <http://www.gnu.org/licenses/>.

'''
Logging utilities. Contains only `set_level`, temporarily changes log level.
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
        