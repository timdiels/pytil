# Copyright (C) 2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
#
# This file is part of pytil.
#
# pytil is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pytil is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pytil.  If not, see <http://www.gnu.org/licenses/>.

'''
Test pytil.iterable
'''

import pytest
from pytil.iterable import sliding_window, partition, is_sorted, flatten

class TestSlidingWindow(object):

    def test_invalid_size(self):
        '''
        - When size < 1, ValueError
        - When size > ilen(iterable), ValueError
        '''
        with pytest.raises(ValueError):
            list(sliding_window(range(5), size=0))
        with pytest.raises(ValueError):
            list(sliding_window(range(5), size=6))

    def test_happy_days(self):
        '''Test various regular inputs'''
        assert list(sliding_window(range(5), size=1)) == [(0,),(1,),(2,),(3,),(4,)]
        assert list(sliding_window(range(5), size=2)) == [(0,1),(1,2),(2,3),(3,4)]
        assert list(sliding_window(range(5), size=3)) == [(0,1,2),(1,2,3),(2,3,4)]
        assert list(sliding_window(range(5), size=4)) == [(0,1,2,3),(1,2,3,4)]
        assert list(sliding_window(range(5), size=5)) == [(0,1,2,3,4)] 

def test_partition():
    assert partition(range(5), lambda x: x % 2) == {
        0: [0,2,4],
        1: [1,3]
    }

def test_is_sorted():
    assert is_sorted(range(7))
    assert not is_sorted((1,4,3))

class TestFlatten(object):

    def test_invalid_times(self):
        with pytest.raises(ValueError):
            '''When times < 0, ValueError'''
            list(flatten([1], times=-1))

    @pytest.mark.parametrize('times', range(6))
    def test_empty(self, times):
        '''When flatten empty, return iter(empty)'''
        assert list(flatten([], times=times)) == []

    def test_happy_days(self):
        '''Test various regular inputs'''
        assert list(flatten([[2, 3], 1, [5, [7, 8]]])) == [2, 3, 1, 5, [7, 8]]
        assert list(flatten([[2, 3], 1, [5, [7, 8]]], times=2)) == [2, 3, 1, 5, 7, 8]
        assert list(flatten([[2, 3], 1, [5, [7, 8]]], times=3)) == [2, 3, 1, 5, 7, 8]
        assert list(flatten([[2, 3], 1, [5, [7, 8]]], times=0)) == [[2, 3], 1, [5, [7, 8]]]

        # Deep things are left alone (not iterators turned into lists or lists turned into sets or ...
        iterator = iter([7, 8])
        assert list(flatten([iter([2, 3]), 1, [{1,2}, iterator]])) == [2, 3, 1, {1,2}, iterator]
