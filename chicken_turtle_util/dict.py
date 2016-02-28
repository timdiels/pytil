# Copyright (C) 2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
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
dict-like extensions, multidict, keydefaultdict
'''

from collections import defaultdict

def invert_multidict(dict_):
    '''
    Invert multi-dict (=multimap)
    
    Parameters
    ----------
    dict_ : {any -> iterable}
        Multi-dict to invert
        
    Returns
    -------
    {any -> {any}}
        Inverted dict
    '''
    result = defaultdict(lambda: set())
    for k, vals in dict_.items():
        for val in vals:
            result[val].add(k)
    return dict(result)

def invert_dict(dict_):
    '''
    Invert dict
    
    Parameters
    ----------
    dict_ : {any -> hashable}
        Dict to invert
        
    Returns
    -------
    {any -> {any}}
        Inverted dict
    '''
    result = defaultdict(lambda: set())
    for k, val in dict_.items():
        result[val].add(k)
    return dict(result)

class keydefaultdict(defaultdict):
    
    '''
    Like defaultdict, but its default value factory takes a key argument
    
    Source: http://stackoverflow.com/a/2912455/1031434
    '''
    
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret
        
def dict_subset(dict_, keys, fragile=True):
    '''
    Get subset of dict as dict
    
    When keys are missing, KeyError is raised.
    
    Parameters
    ----------
    dict_ : dict
        Dict to take subset from.
    keys : iterable of str
        Keys to include in subset.
    fragile : bool
        If True, raise on missing key, else omits missing keys from subset.
    ''' 
    if fragile:
        return {k : dict_[k] for k in keys}
    else:
        return {k : dict_[k] for k in keys if k in dict_}
    
    