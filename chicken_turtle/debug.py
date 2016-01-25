# Copyright (C) 2015-2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
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

'''
Debug utilities
'''

import os
import psutil
from contextlib import contextmanager
import logging
from pprint import pprint

def print_mem():
    process = psutil.Process(os.getpid())
    print('{}MB memory usage'.format(int(process.memory_info().rss / 2**20)))
    
@contextmanager
def log_sql():
    logger = logging.getLogger('sqlalchemy.engine')
    original = logger.level
    logger.setLevel(logging.INFO)
    try:
        yield
    finally:
        logger.setLevel(original)
        
def print_sql_stmt(stmt):
    print(str(stmt).replace('JOIN', '\nJOIN').replace('UNION ', '\nUNION\n').replace('(', '(\n').replace(')', '\n)').replace('GROUP', '\nGROUP'))
    print()

def print_abbreviated_dict(dict_, count=10):
    pprint(dict(list(dict_.items())[:count]))

