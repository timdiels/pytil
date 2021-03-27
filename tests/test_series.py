# Copyright (C) 2016-2021 VIB/BEG/UGent - Tim Diels <tim@diels.me>
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

'Test pytil.series'

from pytil import series as series_
from pytil.series import series_equals, assert_series_equals
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
    assert series_equals(series1, series1)

    series2 = pd.Series([2, 1, 3+1e-8], index=[1,2,3])
    assert series_equals(series1, series2, ignore_order=True, ignore_index=True, all_close=True)
    assert not series_equals(series1, series2, ignore_index=True, all_close=True)

def test_assert_equals():
    '''
    Trivial test assuming the actual equality check is forwarded to
    series.equals
    '''
    series1 = pd.Series([1, 2, 3], index=['i1', 'i2', 'i3'])
    assert_series_equals(series1, series1)

    series2 = pd.Series([2, 1, 3+1e-8], index=[1,2,3])
    assert_series_equals(series1, series2, ignore_order=True, ignore_index=True, all_close=True)
    with pytest.raises(AssertionError):
        assert_series_equals(series1, series2, ignore_index=True, all_close=True)
