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
Utility functions for working with iterables

See also
--------
itertools
more_itertools
toolz.itertoolz
'''

from more_itertools import windowed

def is_sorted(iterable):
    '''
    Get whether iterable is sorted ascendingly

    Parameters
    ----------
    iterable : iterable(comparable)
        Iterable whose ordering to check

    Returns
    -------
    bool
        Whether iterable is sorted

    Notes
    -----
    This is mostly intended for testing/debugging purposes. If you need some input
    sorted, it's usually better to just sort it instead of requiring and
    checking whether it's sorted. If you do need that extra performance, you'll
    probably have to assume without checking. If however, you are checking an
    invariant during testing, this is the function for you.
    '''
    return all(x1 <= x2 for x1, x2 in windowed(iterable, 2))
