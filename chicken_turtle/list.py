# Copyright (C) 2015-2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
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
list-like extensions
'''

from itertools import chain
import collections

def is_sorted(l):
    return all(l[i] <= l[i+1] for i in range(len(l)-1))

def flatten(list_):
    '''
    Flatten one level of a regularly nested list
    
    Parameters
    ----------
    list_ : list-like of list-like
    '''
    return list(chain(*list_))

# Source: http://stackoverflow.com/a/2158532/1031434
def flatten_deep(list_):
    '''
    Flatten list deeply
    
    Irregularly nested lists are flattened as well:
    
    >>> flatten_deep([5, [1,2], 6, [7,[8]]])
    [5,1,2,6,7,8]
    
    Parameters
    ----------
    list_ : iterable of any
        If iterable (except str or bytes), it is flattened, otherwise it's returned as is
    '''
    for item in list_:
        if isinstance(item, collections.Iterable) and not isinstance(item, (str,bytes)):
            for sub in flatten_deep(item):
                yield sub
        else:
            yield item
            
def find(list_, value, key=None):
    if key:
        for x in list_:
            if key(x) == value:
                return x
    else:
        try:
            return list_[list_.index(value)]
        except ValueError:
            return None