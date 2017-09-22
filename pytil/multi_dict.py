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
Multi-dict class, a dict which maps keys to one or more values.
'''

from collections import defaultdict

class MultiDict(object):

    '''
    A multi-dict, a dict which maps keys to one or more values.

    .. warning::

       This is very much a work in progress.

    Parameters
    ----------
    dict_ : ~typing.Dict[~typing.Hashable, ~typing.Set[~typing.Hashable]]
        Dict to create a multi-dict view of. No copy is made. Editing the
        multi-dict, edits the underlying dict. Changes to the underlying dict,
        affect the multi-dict.

    Notes
    -----
    A multi-dict (or multi map) is a dict that maps each key to one or more values.

    Multi-dicts provided by other libraries tend to be more feature rich, while
    this interface is far more conservative. Instead of wrapping, they provide
    an interface that mixes regular and multi-dict access. Additionally, other
    multi-dicts map keys to lists of values, allowing a key to map to the same
    value multiple times.
    '''

    # TODO init should construct a multidict with underlying dict made for the user. To get a view onto an existing dict, add MultiDict.view(dict_)

    # TODO consider using lists instead of sets to allow duplicate values

    # TODO consider allowing both list and set variants, but then creating a
    # dict should not be by init but by 2 static methods after all (one for
    # creating lists, one for set based)

    def __init__(self, dict_):
        self._dict = dict_

    @property
    def dict(self):
        '''
        Get the underlying dict.

        Returns
        -------
        ~typing.Dict[~typing.Hashable, ~typing.Set[~typing.Hashable]]
            The underlying dict.
        '''
        return self._dict

    def invert(self):
        '''
        Invert by swapping each value with its key.

        Returns
        -------
        MultiDict
            Inverted multi-dict.

        Examples
        --------
        >>> MultiDict({1: {1}, 2: {1,2,3}}, 4: {}).invert()
        MultiDict({1: {1,2}, 2: {2}, 3: {2}})
        '''
        result = defaultdict(set)
        for k, val in self.items():
            result[val].add(k)
        return MultiDict(dict(result))

    def items(self):
        return ((k, val) for k, vals in self._dict.items() for val in vals)

    def keys(self):
        return (k for k, vals in self._dict.items() if vals)

    def values(self):
        return (val for vals in self._dict.values() for val in vals) 
