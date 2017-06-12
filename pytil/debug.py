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
Debug utilities. Contains `pretty_memory_info`, formats a memory usage message
'''

import os
import psutil

def pretty_memory_info():
    '''
    Get pretty memory info message

    Returns
    -------
    str
        Memory usage, ...
    '''
    process = psutil.Process(os.getpid())
    return '{}MB memory usage'.format(int(process.memory_info().rss / 2**20))
