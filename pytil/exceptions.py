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
Exception classes and utilities.
'''

def exc_info(exception):
    '''
    Get exc_info tuple from exception.

    See also
    --------
    sys.exc_info
    '''
    return (type(exception), exception, exception.__traceback__)

class UserException(Exception):

    '''
    Exceptional user input/action.
    '''

class InvalidOperationError(Exception):

    '''
    Operation is illegal/invalid in the current state.

    If an invalid argument was given, use `ValueError` instead. An operation can be
    a method/function call or getting/setting an attribute.
    '''
