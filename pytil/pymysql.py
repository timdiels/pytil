# Copyright (C) 2015 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
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
pymysql utilities. Contains only `patch`, patches pymysql to be compatible with numpy and others.
'''

import pymysql
from contextlib import suppress

def patch():
    '''
    Patch bugs and add encoders for other data types to pymysql

    Applied patches:

    - if numpy is installed, add an encoder for np.int64
    '''
    with suppress(ImportError):
        import numpy as np
        pymysql.converters.conversions[np.int64] = pymysql.converters.encoders[int]