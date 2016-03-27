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
sqlalchemy utilities
'''

from chicken_turtle_util import logging as logging_, str as str_
import logging
    
def log_sql():
    '''
    Temporarily log SQL statements
    '''
    return logging_.set_level('sqlalchemy.engine', logging.INFO)
        
def pretty_sql(statement): #TODO replace with proper pretty print that parses sql, take it from other library and just make note of it, don't actually add it here
    '''
    Pretty format sql
    
    Parameters
    ----------
    statement : str or sql expression or Query or anything whose str() returns SQL
        The SQL statement to print
    '''
    replacements = (
        ('INNER JOIN', '\nINNER JOIN'),
        ('FROM', '\nFROM'),
        ('GROUP', '\nGROUP'),
        ('WHERE', '\nWHERE'),
        ('UNION ', '\nUNION\n'),
        ('(', '(\n'),
        (')', '\n)')
    )
    for from_, to in replacements:
        statement = statement.replace(from_, to)
    return str_.multiline_strip(statement, drop_empty=True)
