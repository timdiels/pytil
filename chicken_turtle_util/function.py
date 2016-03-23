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
Function utilities
'''

from functools import reduce as reduce

def compose(*functions):
    '''
    Compose functions
    
    Like the `o` operator in math.
    
    Parameters
    ----------
    functions : [any -> any]
        List of functions to compose. You need to supply at least 1.
    
    Returns
    -------
    any -> any
        Function composed of `functions`
    
    Examples
    --------
    `compose(f1, f2)` is equivalent to `f1 o f2`, or to `lambda x: f1(f2(x))`
    '''
    apply = lambda x, y: y(x)
    return lambda x: reduce(apply, functions, x)

