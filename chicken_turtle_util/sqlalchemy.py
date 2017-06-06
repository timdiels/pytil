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
sqlalchemy utilities. Contains pretty sql formatting and temporarily enabling sqlalchemy logging
'''

from chicken_turtle_util import logging as logging_
import logging
import sqlparse

def log_sql():
    '''
    Temporarily log SQL statements

    Examples
    --------
    >>> with log_sql():
    ...     pass # sqlalchemy log level is set to INFO in this block 
    '''
    return logging_.set_level('sqlalchemy.engine', logging.INFO)

def pretty_sql(statement):
    '''
    Pretty format sql

    Parameters
    ----------
    statement : hasattr('__str__')
        anything whose str() returns SQL

    Returns
    -------
    str
        Pretty formatted SQL
    '''
    return sqlparse.format(str(statement), reindent=True, keyword_case='upper')
