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
from functools import wraps

# TODO later: All is done, except: adjust API doc, README changelog and perhaps feature list. Commit (NOT git add ., there are other pending changes)

def call_repr(name=None, exclude_args=()):
    '''
    Add function call `repr` argument to function 
    
    Function calls are uniquely mapped to strings (it's deterministic and
    injective) and supplied to the decorated function as the `call_repr_` keyword
    argument. The manner and order in which the arguments are supplied are
    ignored. The format is
    ``{f.__module__}.{f.__qualname__}(arg_name=repr(arg_value), ...)``.
    
    Parameters
    ----------
    name : str or None
        The fully qualified name of the function prefixed with the module name
        its defined in. If ``None``, it is derived from `f`.
        
        If `f` is a nested function with an ancestor that takes arguments, it is
        no longer guaranteed that the returned string is unique. In that case,
        you should specify the name manually using the `call_repr_` of the
        ancestor. See 'parametrised nesting' in the examples section below.
    exclude_args : iterable(str)
        Names of arguments to exclude from the function call repr
        
    Returns
    -------
    function -> decorated_function
        Function which decorates functions with the `call_repr` argument.
    
    See also
    --------
    get_call_repr: Get `repr` of function call
    
    Examples
    --------
    >>> # package/module.py
    >>> @call_repr()
    ... def f(a, b=2, *myargs, call_repr_, x=1, **mykwargs):
    ...     return call_repr_
    ...
    >>> f(1)
    'package.module.f(*args=(), a=1, b=2, x=1)'
    >>> f(1, 2, 3, x=10, y=20)
    'package.module.f(*args=(1,), a=1, b=2, x=10, y=20)'
    >>> @call_repr(name='my.func')
    ... def g(call_repr_):
    ...     return call_repr_
    ...
    >>> g()
    'my.func()'
    >>> @call_repr(exclude_args={'a'})
    ... def h(a, b, call_repr_):
    ...     return call_repr_
    ...
    >>> h(1, 2)
    'package.module.h(b=2)'
    
    With parametrised nesting you may want to:
    
    >>> @call_repr()
    ... def f(a, b, call_repr_):
    ...     @call_repr(name=call_repr_ + '::g')
    ...     def g(x, call_repr_):
    ...         return call_repr_
    ...
    >>> f(1,2)('x')
    "package.module.f(a=1, b=2)::g(x='x')"
    
    Optional arguments are always included and the order in which arguments
    appear in the function definition is ignored:
    
    >>> @call_repr()
    ... def f(b, a=None, call_repr_):
    ...     return call_repr_
    ...
    >>> f(1)
    'package.module.f(a=None, b=1)'
    '''
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            kwargs['call_repr_'] = None  # otherwise call_args fails on functions with call_repr_ as required arg
            kwargs['call_repr_'] = get_call_repr(f, args, kwargs, name, set(exclude_args) | {'call_repr_'})
            return f(*args, **kwargs)
        return decorated
    return decorator
    
def get_call_repr(f, args=(), kwargs={}, name=None, exclude_args=()):
    '''
    Get `repr` of function call
    
    Function calls are uniquely mapped to strings (it's deterministic and
    injective). The manner and order in which the arguments are supplied are
    ignored. The format is
    ``{f.__module__}.{f.__qualname__}(arg_name=repr(arg_value), ...)``.
    
    Parameters
    ----------
    f
        Function of the function call
    args : iterable(any)
        Arguments of the function call
    kwargs : {str => any}
        Keyword arguments of the function call
    name : str or None
        The fully qualified name of the function prefixed with the module name
        its defined in. If ``None``, it is derived from `f`.
        
        If `f` is a nested function with an ancestor that takes arguments, it is
        no longer guaranteed that the returned string is unique. In that case,
        you should specify the name manually using `get_call_repr` on the
        ancestor. See 'parametrised nesting' in the examples section below.
    exclude_args : iterable(str)
        Names of arguments to exclude from the function call repr
    
    Returns
    -------
    str
        The repr of the call
        
    See also
    --------
    call_repr: Add function call `repr` argument to function
    
    Examples
    --------
    >>> # package/module.py
    >>> def f(a, b=2, *myargs, x=1, **mykwargs):
    ...     pass
    ...
    >>> get_call_repr(f, [1])
    'package.module.f(*args=(), a=1, b=2, x=1)'
    >>> get_call_repr(f, [1, 2, 3], dict(x=10, y=20))
    'package.module.f(*args=(1,), a=1, b=2, x=10, y=20)'
    >>> get_call_repr(f, [1], dict(b=3, x=10, y=20))
    'package.module.f(*args=(), a=1, b=3, x=10, y=20)'
    >>> get_call_repr(f, [1], name='my.func')
    'my.func(*args=(), a=1, b=2, x=1)'
    >>> get_call_repr(f, [1], exclude_args={'a'})
    'package.module.h(b=2)'
    
    With parametrised nesting you may want to:
    
    >>> def f(a, b):
    ...     def g(x):
    ...         pass
    ...
    >>> g = f(1,2)
    >>> f_call_repr = get_call_repr(f, [1,2])
    >>> get_call_repr(g, ['x'], name=f_call_repr + '::g')
    "package.module.f(a=1, b=2)::g(x='x')"
    
    Optional arguments are always included and the order in which arguments
    appear in the function definition is ignored:
    
    >>> def f(b, a=None):
    ...     pass
    ...
    >>> get_call_repr(f, [1])
    'package.module.f(a=None, b=1)'
    '''
    kwargs = call_args(f, args, kwargs)
    if not name:
        name = '{}.{}'.format(f.__module__, f.__qualname__)
    for arg in exclude_args:
        if arg in kwargs:
            del kwargs[arg]
    args = ', '.join('{}={!r}'.format(key, value) for key, value in sorted(kwargs.items()))
    return '{}({})'.format(name, args)

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
