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
Test chicken_turtle_util.inspect
'''

from chicken_turtle_util.inspect import call_repr, get_call_repr, call_args

def test_call_repr():
    @call_repr()
    def f(a, b=2, *myargs, call_repr_, x=1, **mykwargs):
        return call_repr_
    
    name = 'chicken_turtle_util.tests.test_inspect.test_call_repr.<locals>.f'
    assert f(1) == name + '(*args=(), a=1, b=2, x=1)'
    assert f(1, 2, 3, x=10, y=20) == name + '(*args=(3,), a=1, b=2, x=10, y=20)'
    
    @call_repr(name='my.func')
    def g(b, a, call_repr_):
        return call_repr_
    assert g(1, 2) == 'my.func(a=2, b=1)'
    
    g = call_repr(name='g', exclude_args={'a'})(g.__wrapped__)
    assert g(1, 2) == 'g(b=1)'
    
    g = call_repr(name='g', exclude_args={'a', 'b'})(g.__wrapped__)
    assert g(1, 2) == 'g()'
    
def test_get_call_repr(): #TODO if this private function will never be made public, remove this test
    def f(b, a, k=None):
        pass
    
    name = 'chicken_turtle_util.tests.test_inspect.test_get_call_repr.<locals>.f'
    assert get_call_repr(f, [1, 2]) == name + '(a=2, b=1, k=None)'
    assert get_call_repr(f, [1, 'str']) == name + "(a='str', b=1, k=None)"
    assert get_call_repr(f, [1, 2], dict(k=-3)) == name + "(a=2, b=1, k=-3)"
    assert get_call_repr(f, [1, 2], name='my.func') == 'my.func(a=2, b=1, k=None)'
    assert get_call_repr(f, [1, 2], exclude_args={'a'}) == name + '(b=1, k=None)'
    assert get_call_repr(f, [1, 2], exclude_args={'a', 'b'}) == name + '(k=None)'
    
def test_call_args():
    def f(a=1, *args, k=None, **kwargs):
        pass
    
    assert call_args(f) == {'a': 1, 'k': None, '*args': ()}
    assert call_args(f, [3]) == {'a': 3, 'k': None, '*args': ()}
    assert call_args(f, [3], dict(k='some')) == {'a': 3, 'k': 'some', '*args': ()}
    assert call_args(f, [3, 4]) == {'a': 3, 'k': None, '*args': (4,)}
    assert call_args(f, [], dict(other='some')) == {'a': 1, 'k': None, 'other': 'some', '*args': ()}
    
    # When an arg appears in kwargs instead of args, deal with it
    def g(a, k=None):
        pass
    assert call_args(g, [], dict(a=1)) == {'a': 1, 'k': None}