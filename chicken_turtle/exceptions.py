# Copyright (C) 2015 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
# 
# This file is part of Chicken Turtle.
# 
# Chicken Turtle is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Chicken Turtle is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with Chicken Turtle.  If not, see <http://www.gnu.org/licenses/>.

from contextlib import contextmanager
import logging

'''
Exception handling helpers
'''

def prefix_with_name(obj):
    '''
    Prefix str(obj) with its class name
    
    Parameters
    ----------
    obj : object
        Exception object (or any other type of object)
        
    Returns
    -------
    str
    '''
    '{}: {}'.format(obj.__class__.__name__, obj)
   
@contextmanager 
def log_exception_msg(logger, exception_type, level=logging.WARNING):
    '''
    Suppress and log exception using its message, no trace is printed
    
    Parameters
    ----------
    logger : logging.Logger
        Logger to log with
    exception_type : subclass of Exception, or Exception
        Type of exceptions to log and suppress
    level
        Log level to use
    '''
    try:
        yield
    except exception_type as ex:
        logger.log(level, prefix_with_name(ex))
        