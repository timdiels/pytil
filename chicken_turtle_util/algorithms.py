# Copyright (C) 2015 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
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
Various algorithms
'''

from sklearn.utils.extmath import cartesian
from collections_extended import bag, frozenbag
import numpy as np

def spread_points_in_hypercube(point_count, dimension_count):
    '''
    Place `n` points in a unit hypercube such that the minimum distance between
    points is approximately maximal.
    
    Euclidean distance is used.
    
    Parameters
    ----------
    point_count : int
        Number of points to pick
    dimension_count : int
        Number of dimensions of the hypercube
        
    Returns
    -------
    np.array(shape=(point_count, dimension_count))
        Points spread approximately optimally across the hypercube.
        
    Raises
    ------
    ValueError
        When `point_count` < 0 or when `dimension_count` < 1
        
    Notes
    -----
    The exact solution to this problem is known for only a few `n`.
    
    References
    ----------
    .. [1] http://stackoverflow.com/a/2723764/1031434
    '''
    # Current implementation simply puts points in a grid
    if point_count < 0:
        raise ValueError('point_count must be at least 0')
    if dimension_count < 1:
        raise ValueError('dimension_count must be at least 1')
    if point_count == 0:
        return np.empty(shape=(0,dimension_count))
    side_count = np.ceil(point_count ** (1/dimension_count)) # number of points per side
    points = np.linspace(0, 1, side_count)
    points = cartesian([points]*dimension_count)
    return np.random.permutation(points)[:point_count] #XXX permutation is unnecessary

class _Bin(object):
    def __init__(self):
        self._items = []
        self._weights_sum = 0
        
    def add(self, item, weight):
        self._items.append(item)
        self._weights_sum += weight
        
    @property
    def items(self):
        return self._items
    
    @property
    def weights_sum(self):
        return self._weights_sum

def multi_way_partitioning(items, bin_count):
    '''
    Greedily divide weighted items equally across bins (multi-way partition problem)
    
    This approximately minimises the difference between the largest and smallest
    sum of weights in a bin.
    
    Parameters
    ----------
    items : iterable((item :: any) : (weight :: number))
        Weighted items
    bin_count : int
        Number of bins
        
    Returns
    -------
    bins : bag(bin :: frozenbag(item :: any))
        Bins with the items
        
    References
    ----------
    .. [1] http://stackoverflow.com/a/6855546/1031434 describes the greedy algorithm
    .. [2] http://ijcai.org/Proceedings/09/Papers/096.pdf defines the problem and describes algorithms
    '''
    bins = [_Bin() for _ in range(bin_count)]
    for item, weight in sorted(items, key=lambda x: x[1], reverse=True):
        bin_ = min(bins, key=lambda bin_: bin_.weights_sum) 
        bin_.add(item, weight)
    return bag(frozenbag(bin_.items) for bin_ in bins)
    

