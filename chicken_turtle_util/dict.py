# Copyright (C) 2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
#
# This file is part of Chicken Turtle Util.
#
# Chicken Turtle Util is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Chicken Turtle Util is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Chicken Turtle Util.  If not, see <http://www.gnu.org/licenses/>.

'''
`dict` utilities
'''

from collections import defaultdict
from pprint import pprint
from more_itertools import take

def pretty_print_head(dict_, count=10):
    '''
    Pretty print some items of a dict

    For an unordered dict, `count` arbitrary items will be printed. 

    Parameters
    ----------
    dict_ : dict
        Dict to print from
    count : int, optional
        Number of items to print.

    Raises
    ------
    ValueError
        When ``count < 1``
    '''
    if count < 1:
        raise ValueError('`count` must be at least 1')
    pprint(dict(take(count, dict_.items())))

# Idea and implementation comes from: http://stackoverflow.com/a/2912455/1031434
class DefaultDict(defaultdict):

    '''
    Replacement for `collections.defaultdict`, its default value factory takes a
    key argument

    Parameters
    ----------
    default_factory : (key :: any) -> (value :: any)
        Function that is called with the missing key and returns the default
        value to use for it
    '''

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret

def invert(dict_):
    '''
    Invert dict by swapping each value with its key

    Parameters
    ----------
    dict_ : {hashable => hashable}
        Dict to invert

    Returns
    -------
    {hashable => {hashable}}
        `dict_` copy with key and value swapped, a multi-dict (as some keys in
        `dict_` may have had the same value).

    See also
    --------
    MultiDict : A mutable multi-dict view of a ``{hashable => {hashable}}`` dict.

    Notes
    -----
    If your dict never has 2 keys mapped to the same value, you can convert it
    to a ``{hashable => any}`` dict using::

        from chicken_turtle_util.multi_dict import MultiDict
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

def assign(destination, source):
    '''
    Assign one dict to the other through mutations

    Roughly put, ``destination := source``. More formally, after the call,
    ``destination == source`` is true and ``id(destination)`` is unchanged.

    Parameters
    ----------
    destination : dict
        dict to assign to
    source : dict
        dict to assign from

    Examples
    --------
    >>> import chicken_turtle_util.dict as dict_
    >>> destination = {1: 2, 3: 4}
    >>> source = {3: 5, 6: 7}
    >>> dict_.assign(destination, source)
    >>> assert destination == {3: 5, 6: 7} 
    '''
    # remove extra
    for key in destination.keys() - source.keys():
        del destination[key]

    # assign the rest
    for key, value in source.items():
        destination[key] = value
