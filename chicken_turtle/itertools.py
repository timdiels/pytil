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
itertools additions
'''

from itertools import islice

# Source: http://stackoverflow.com/a/6822773/1031434
def window(iter_, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(iter_)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result    
    for elem in it:
        result = result[1:] + (elem,)
        yield result
        
def bifilter(iter_, condition):
    '''
    Split iterable on condition
    
    Parameters
    ----------
    iter_ : iterable of any
    condition : function(seq_item) -> bool
    
    Returns
    -------
    passes, fails : list of any, list of any
        `passes` contains the items for which condition was `True`, `fails` returns the complement.
    '''
    passes = []
    fails = []
    for term in iter_:
        if condition(term):
            passes.append(term)
        else:
            fails.append(term)
    return passes, fails

def bifilter_tuples(iter_):
    '''
    Split iterable of tuples on bool in tuple
    
    Parameters
    ----------
    iter_ : iterable of (any, bool)
    
    Returns
    -------
    passes, fails : list of any, list of any
        `passes` contains first element of each tuple for which its second
        element is `True`, `fails` returns the complement.
    '''
    passes = []
    fails = []
    for term in iter_:
        if term[1]:
            passes.append(term[0])
        else:
            fails.append(term[0])
    return passes, fails