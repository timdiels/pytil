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
Utility functions for working with iterables. `sliding_window`, ...

See also
--------
itertools
more_itertools
'''

from itertools import islice
from collections import defaultdict
import collections

# The implementation comes from: http://stackoverflow.com/a/6822773/1031434
def sliding_window(iterable, size=2):
    '''
    Iterate using a sliding window

    Parameters
    ----------
    iterable : iterable(any)
        Iterable to slide a window across
    size : int, optional
        Window size

    Yields
    -------
    (any, ...)
        Iterator slices of size `size`, taken from start to end through the iterator.

    Raises
    ------
    ValueError
        When ``ilen(iterable) < size or size < 1``

    See also
    --------
    more_itertools.chunked : Divide iterable into (non-overlapping) chunks of given size

    Examples
    --------
    >>> list(sliding_window(range(4)))
    [(0,1), (1,2), (2,3)]

    >>> list(sliding_window(range(4), size=3))
    [(0,1,2), (1,2,3)]

    >>> list(sliding_window(range(1)))
    []
    '''
    if size < 1:
        raise ValueError('Window `size` must be at least 1')
    it = iter(iterable)
    result = tuple(islice(it, size))
    if len(result) < size:
        raise ValueError('Window larger than `ilen(iterable)`')
    yield result    
    for elem in it:
        result = result[1:] + (elem,)
        yield result

def partition(iterable, key):
    '''
    Split iterable into partitions

    Parameters
    ----------
    iterable : iterable(item :: any)
        Iterable to split into partitions
    key : (item :: any) -> (partition_id :: any)
        Function that assigns an item of the iterable to a partition

    Returns
    -------
    partitioning : {(partition_id :: any) : partition :: [item :: any]} 
        Partitioning. Ordering of items is maintained within each `partition`.
        I.e. each `partition` is a subsequence of `iterable`.
    '''
    partitioning = defaultdict(list)
    for item in iterable:
        partitioning[key(item)].append(item)
    return partitioning

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
    '''
    return all(x1 <= x2 for x1, x2 in sliding_window(iterable))

# Implementation based on http://stackoverflow.com/a/2158532/1031434
def flatten(iterable, times=1):
    '''
    Flatten shallowly zero or more times

    Does not flatten `str` and `bytes`. Order is stably maintained (i.e. no 2
    items swap places, even if they're equal).

    Parameters
    ----------
    iterable : iterable(any) except str or bytes
        Iterable to flatten. May be any iterable other than `str` or `bytes`. May have irregular depth. 
    times : int, optional
        The number of times to flatten shallowly or, equivalently, the number of
        levels of depth to remove. Should be 0 or more.

    Yields
    -------
    any
        Items of iterable flattened to depth ``depth(iterable) - times``

    Raises
    ------
    ValueError
        If input is invalid.

    Examples
    --------
    >>> list(flatten([[2, 3], 1, [5, [7, 8]]]))
    [2, 3, 1, 5, [7, 8]]

    >>> list(flatten([[2, 3], 1, [5, [7, 8]]], times=2))
    [2, 3, 1, 5, 7, 8]

    >>> list(flatten([[2, 3], 1, [5, [7, 8]]], times=3))
    [2, 3, 1, 5, 7, 8]

    >>> flatten([iter([2, 3]), 1, [5, iter([7, 8])]])
    iter([2, 3, 1, 5, iter([7, 8])])

    >>> list(flatten([[2, 3], 1, [5, [7, 8]]], times=0))
    [[2, 3], 1, [5, [7, 8]]]
    '''
    if not _is_sensibly_iterable(iterable):
        raise ValueError('`iterable` is not iterable or is `str` or `bytes`')
    if times < 0:
        raise ValueError('times < 0: {}'.format(times))
    for x in _flatten(iterable, times+1):  # times+1 as _flatten includes unpacking the passed iterable in times
        yield x

def _flatten(item, times):
    assert times >= 0
    if times > 0 and _is_sensibly_iterable(item):
        for x in item:
            for y in _flatten(x, times-1):
                yield y
    else:
        yield item

def _is_sensibly_iterable(obj):
    return isinstance(obj, collections.Iterable) and not isinstance(obj, (str,bytes))
