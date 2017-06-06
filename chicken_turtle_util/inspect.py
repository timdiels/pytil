# Copyright (C) 2015, 2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
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
Similar to `inspect` module. Contains only function call inspect utilities
'''

import inspect

def call_args(f, args=(), kwargs={}):
    '''
    Get function call arguments as a single dict

    Parameters
    ----------
    f : function
        The function of the function call
    args : iterable(any)
        Arguments of the function call
    kwargs : {str => any}
        Keyword arguments of the function call

    Returns
    -------
    {arg_name :: str => arg_value :: any}
        Dict of arguments including `args`, `kwargs` and any missing optional
        arguments of `f`.

    Examples
    --------
    >>> def f(a=1, *my_args, k=None, **kwargs):
    ...     pass
    ...
    >>> call_args(f)
    {'a': 1, 'k': None, '*args': ()}
    >>> call_args(f, [3])
    {'a': 3, 'k': None, '*args': ()}
    >>> call_args(f, [3], dict(k='some'))
    {'a': 3, 'k': 'some', '*args': ()}
    >>> call_args(f, [3, 4])
    {'a': 3, 'k': None, '*args': (4,)}
    >>> call_args(f, dict(other='some'))
    {'a': 1, 'k': None, 'other': 'some', '*args': ()}
    >>> def g():
    ...     pass
    ...
    >>> call_args(g)
    {}
    '''
    kwargs = inspect.getcallargs(f, *args, **kwargs)
    argspec = inspect.getfullargspec(f)
    if argspec.varargs:
        kwargs['*args'] = kwargs[argspec.varargs]
        del kwargs[argspec.varargs]
    if argspec.varkw:
        kwargs.update(kwargs[argspec.varkw])
        del kwargs[argspec.varkw]
    return kwargs
