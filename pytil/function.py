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
Function manipulation, like functools. Contains only `compose`, compose functions.
'''

from functools import reduce as reduce

def compose(*functions):
    '''
    Compose functions

    Like the ``o`` operator in math.

    Parameters
    ----------
    functions : collection(any -> any)
        Collection of one or more functions to compose.

    Returns
    -------
    any -> any
        Function composed of `functions`

    Raises
    ------
    ValueError
        When ``len(functions) < 1``

    Examples
    --------
    ``compose(f1, f2)`` is equivalent to ``f1 o f2``, or to ``lambda x: f1(f2(x))``
    '''
    if not functions:
        raise ValueError('Must supply at least one function to `compose`')
    apply = lambda x, y: y(x)
    return lambda x: reduce(apply, reversed(functions), x)
