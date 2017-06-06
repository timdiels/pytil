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
Test chicken_turtle_util.series
'''

from chicken_turtle_util import series as series_
import pandas as pd
import pytest

def test_invert():
    index = pd.Index([4,5,6], name='index_name')
    inverted = series_.invert(pd.Series([1,2,3], index=index, name='named'))
    expected = pd.Series([4,5,6], index=[1,2,3], name='index_name')
    assert inverted.equals(expected)
    assert inverted.name == expected.name

def test_equals():
    '''
    Trivial test assuming the actual equality check is forwarded to
    data_frame.equals
    '''
    series1 = pd.Series([1, 2, 3], index=['i1', 'i2', 'i3'])
    assert series_.equals(series1, series1)

    series2 = pd.Series([2, 1, 3+1e-8], index=[1,2,3])
    assert series_.equals(series1, series2, ignore_order=True, ignore_index=True, all_close=True)
    assert not series_.equals(series1, series2, ignore_index=True, all_close=True)

def test_assert_equals():
    '''
    Trivial test assuming the actual equality check is forwarded to
    series.equals
    '''
    series1 = pd.Series([1, 2, 3], index=['i1', 'i2', 'i3'])
    series_.assert_equals(series1, series1)

    series2 = pd.Series([2, 1, 3+1e-8], index=[1,2,3])
    series_.assert_equals(series1, series2, ignore_order=True, ignore_index=True, all_close=True)
    with pytest.raises(AssertionError):
        series_.assert_equals(series1, series2, ignore_index=True, all_close=True)

def test_split():
    '''
    Trivial test assuming the actual split is done by data_frame.split_array_like
    '''
    actual = series_.split(pd.Series([[1,2],[2,3,4],[]]))
    expected = pd.Series([1,2,2,3,4])
    series_.assert_equals(actual, expected, ignore_index=True)
