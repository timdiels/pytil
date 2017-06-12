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
Exception classes: `UserException` and `InvalidOperationError`.

If you miss the ability to pass args to any of these exceptions, note that you actually can. For example:

>>> ex = Exception(1, 2, 3)
>>> ex.args
(1, 2, 3)

You can only use positional arguments though.
'''

def exc_info(exception):
    '''
    Get exc_info tuple from exception
    '''
    return (type(exception), exception, exception.__traceback__)

class UserException(Exception):

    '''
    Exception with message to show the user.

    Parameters
    ----------
    message : str
        User-friendly message
    '''

    def __init__(self, message, *args):
        super().__init__(message, *args)

class InvalidOperationError(Exception):
    '''
    When an operation is illegal/invalid (in the current state), regardless of
    what arguments you throw at it.

    An operation is a method/function call, the getting or setting of an attribute.

    When the issue is with an argument, use ValueError, not this.
    '''
