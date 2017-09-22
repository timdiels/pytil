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
`python:dict` utilities.
'''

from collections import defaultdict
from pprint import pprint
from more_itertools import take

def pretty_print_head(dict_, count=10): #TODO only format and rename to pretty_head
    '''
    Pretty print some items of a dict.

    For an unordered dict, ``count`` arbitrary items will be printed.

    Parameters
    ----------
    dict_ : ~typing.Dict
        Dict to print from.
    count : int
        Number of items to print.

    Raises
    ------
    ValueError
        When ``count < 1``.
    '''
    if count < 1:
        raise ValueError('`count` must be at least 1')
    pprint(dict(take(count, dict_.items())))

# Idea and implementation comes from: http://stackoverflow.com/a/2912455/1031434
class DefaultDict(defaultdict):

    '''
    Default dict whose factory takes a key argument.

    A replacement for `collections.defaultdict`.

    Parameters
    ----------
    default_factory : ~typing.Callable[[~typing.Any], ~typing.Any]
        Function that is called with the missing key and returns the default
        value to use for it.
    '''

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret

def invert(dict_): #TODO return a MultiDict right away
    '''
    Invert dict by swapping each value with its key.

    Parameters
    ----------
    dict_ : ~typing.Dict[~typing.Hashable, ~typing.Hashable]
        Dict to invert.

    Returns
    -------
    ~typing.Dict[~typing.Hashable, ~typing.Set[~typing.Hashable]]
        Dict with keys and values swapped.

    See also
    --------
    pytil.multi_dict.MultiDict : Multi-dict view of a ``Dict[Hashable, Set[Hashable]]`` dict.

    Notes
    -----
    If your dict never has 2 keys mapped to the same value, you can convert it
    to a ``Dict[Hashable, Hashable]`` dict using::

        from pytil.multi_dict import MultiDict
        inverted_dict = dict(MultiDict(inverted_dict))

    Examples
    --------
    >>> invert({1: 2, 3: 4})
    {2: {1}, 4: {3}}

    >>> invert({1: 2, 3: 2, 4: 5})
    {2: {1,3}, 5: {4}}
    '''
    result = defaultdict(lambda: set())
    for k, val in dict_.items():
        result[val].add(k)
    return dict(result)
