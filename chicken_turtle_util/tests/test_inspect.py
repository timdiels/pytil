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

from chicken_turtle_util.inspect import call_args

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
