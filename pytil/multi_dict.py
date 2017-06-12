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
multi-dict utilities. Multi-dicts can map keys to multiple values.

A multi-dict (or multi map) is a dict that maps each key to one or more values.
'''

from collections import defaultdict

class MultiDict(object):

    '''
    A multi-dict view of a ``{hashable => {hashable}}`` dict.

    A light wrapper offering a few methods for working with multi-dicts.

    Parameters
    ----------
    dict_ : {hashable => {hashable}}
        Dict to access as a multi-dict

    Notes
    -----
    A multi-dict (or multi map) is a dict that maps each key to one or more values.

    ``MultiDict``\ s provided by other libraries tend to be more feature rich, while
    this interface is far more conservative. Instead of wrapping, they provide
    an interface that mixes regular and multi-dict access. Additionally, other
    ``MultiDict``\ 's map keys to lists of values, allowing a key to map to the same
    value multiple times.
    '''

    def __init__(self, dict_):
        self._dict = dict_

    @property
    def dict(self):
        '''
        Get the underlying dict

        Returns
        -------
        {hashable => {hashable}}
        '''
        return self._dict

    def invert(self):
        '''
        Invert by swapping each value with its key.

        Parameters
        ----------
        dict_ : {hashable => {hashable}}
            Multi-dict to invert

        Returns
        -------
        {hashable => {hashable}}
            `dict_` copy with key and value swapped.

        Examples
        --------
        >>> invert({1: {1}, 2: {1,2,3}}, 4: {})
        {1: {1,2}, 2: {2}, 3: {2}}
        '''
        result = defaultdict(set)
        for k, val in self.items():
            result[val].add(k)
        return dict(result)

    def items(self):
        return ((k, val) for k, vals in self._dict.items() for val in vals)

    def keys(self):
        return (k for k, vals in self._dict.items() if vals)

    def values(self):
        return (val for vals in self._dict.values() for val in vals) 
