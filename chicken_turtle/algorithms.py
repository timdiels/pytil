# Copyright (C) 2015 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
# 
# This file is part of Chicken Turtle.
# 
# Chicken Turtle is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Chicken Turtle is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with Chicken Turtle.  If not, see <http://www.gnu.org/licenses/>.

'''
Various efficient algorithms
'''

from sklearn.utils.extmath import cartesian
import math
import numpy as np

def _locate_bin(bins, n):
    """
    Find the bin where list n has ended up: Follow bin references until
    we find a bin that has not moved.
    """
    while bins[n] != n:
        n = bins[n]
    return n
    
# TODO test both overlapping set merge funcs
# TODO test performance compared to original alg

# Original implementation by http://stackoverflow.com/users/699305/alexis
# Found here http://stackoverflow.com/a/9453249/1031434
# Outperformed all other algorithms on python3.4 on a wide range of inputs
# Adjusted to handle named sets
def merge_overlapping_named_sets(sets):
    '''
    Merge named sets that overlap.
    
    Merge sets that overlap, keep other sets unchanged. 
    
    >>> merge_overlapping_named_sets([({'a'}, {1,2}), ({'b'}, set()), ({'c'}, {2,3}), ({'d'}, {4,5,6}), (set(), {6,7})])
    [({'a','c'}, {1,2,3}), ({'d'}, {4,5,6,7})]
    
    Parameters
    ----------
    sets : iterable of (names : {any}, values : {any})
        `names` is a set of names assigned to the set, `values`. Tuples with
        empty `values` will be ignored (and will not appear in the output).
        `names` may be the empty set and may show up in the output.
    
    Returns
    -------
    iterable of (names : {any}, values : {any})
        Order of input tuples in `sets` might not be preserved.
    '''
    data = list(sets)
    bins = list(range(len(data)))  # Initialize each bin[n] == n
    nums = dict()
    
    for r, row in enumerate(data):
        if not row[1]:
            data[r] = None
        else:
            for num in row[1]:
                if num not in nums:
                    # New number: tag it with a pointer to this row's bin
                    nums[num] = r
                    continue
                else:
                    dest = _locate_bin(bins, nums[num])
                    if dest == r:
                        continue # already in the same bin
    
                    if dest > r:
                        dest, r = r, dest   # always merge into the smallest bin
    
                    tup = data[r]
                    data[dest][0].update(tup[0])
                    data[dest][1].update(tup[1])
                    data[r] = None
                    # Update our indices to reflect the move
                    bins[r] = dest
                    r = dest 

    # Filter out the empty bins
    return (m for m in data if m)

def merge_overlapping_sets(sets):
    '''
    Merge sets that overlap.
    
    Merge sets that overlap, keep other sets unchanged. 
    
    >>> merge_overlapping_named_sets([{1,2}, set(), {2,3}, {4,5,6}, {6,7}])
    [{1,2,3}, {4,5,6,7}]
    
    Parameters
    ----------
    sets : iterable of {any}
        Empty sets in the input will be ignored.
    
    Returns
    -------
    iterable of {any}
        Order of input tuples in `sets` might not be preserved.
    '''
    merged_named_sets = merge_overlapping_named_sets((set(), set_) for set_ in sets)
    return (set_ for names, set_ in merged_named_sets)

def spread_points_in_hypercube(point_count, dim_count):
    '''
    Approximate a spreading of `n` points in a unit hypercube of given dimension.
    
    Euclidean distance is used.
    
    Note that the exact solution to this problem is known for only a few `n`.
    
    Related: http://stackoverflow.com/a/2723764/1031434
    
    Parameters
    ----------
    point_count : int-like
        Number of points to pick
    dim_count : int-like
        Number of dimensions of the hypercube
        
    Returns
    -------
    array-like
        Points spread approximately optimally in the hypercube. I.e. each point
        component will lie in the interval [0,1].
    '''
    # Current implementation simply puts points in a grid
    side_count = math.ceil(point_count ** (1/dim_count)) # number of points per side #XXX use np.ceil instead
    points = np.linspace(0, 1, side_count)
    points = cartesian([points]*dim_count)
    return np.random.permutation(points)[:point_count]
    