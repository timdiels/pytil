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
Test pytil.data_frame 
'''

import pytil.data_frame as df_
from pytil.data_frame import replace_na_with_none, split_array_like
from itertools import product
import pandas as pd
import numpy as np
import pytest

class TestReplaceNAWithNone(object):

    @pytest.fixture
    def df(self):
        return pd.DataFrame({
            'a' : ['magic', np.nan, 2],
            'word' : [np.nan, np.nan, np.nan],
            5 : [7, 8, 9]  
        })

    @pytest.fixture    
    def df_replaced(self):
        return pd.DataFrame({
            'a' : ['magic', None, 2],
            'word' : [None, None, None],
            5 : [7, 8, 9]  
        })

    def test_inplace(self, df, df_replaced):
        '''When df contains NaN and inplace=False, df contains NaN, return has NaN replaced'''
        df_original = df.copy()
        retval = replace_na_with_none(df)
        assert df.equals(df_original)
        assert retval.equals(df_replaced)

class TestSplitArrayLike(object):

    @pytest.fixture
    def df(self):
        return pd.DataFrame({
            'check': [1, 1, 2, 3],
            'a': [[1, 2], [1, 2], [1], []],
            'b': [[1], [3, 4, 5], [1, 2], [5,6]]
        })

    @pytest.fixture
    def df_split_a_b(self):
        df = pd.DataFrame({
            'check': [1, 1, 1, 1, 1, 1, 1, 1, 2, 2],
            'a': [1, 2, 1, 1, 1, 2, 2, 2, 1, 1],
            'b': [1, 1, 3, 4, 5, 3, 4, 5, 1, 2]
        }, dtype=object)
        df['check'] = df['check'].astype(int)
        return df

    @pytest.fixture
    def df_split_a(self):
        df = pd.DataFrame({
            'check': [1, 1, 1, 1, 2],
            'a': [1, 2, 1, 2, 1],
            'b': [[1], [1], [3, 4, 5], [3, 4, 5], [1, 2]]
        }, dtype=object)
        df['check'] = df['check'].astype(int)
        return df

    def test_split_a_b(self, df, df_split_a_b):
        '''When split on 'a' and 'b', correct split'''
        assert split_array_like(df, ('a', 'b')).equals(df_split_a_b) # Note: test should allow index to differ
        assert split_array_like(df, iter(('a', 'b'))).equals(df_split_a_b)
        assert split_array_like(df.drop('check', axis=1)).equals(df_split_a_b.drop('check', axis=1))

    def test_split_a(self, df, df_split_a):
        '''When split on 'a', correct split'''
        assert split_array_like(df, 'a').equals(df_split_a)
        assert split_array_like(df, ('a',)).equals(df_split_a)

class _Object(object):

    '''
    object that equals those with same id
    '''

    def __init__(self, id_):
        self._id = id_

    def __repr__(self):
        return '_Object({})'.format(self._id)

    def __eq__(self, other):
        return isinstance(other, _Object) and self._id == other._id

class TestEquals(object):

    #TODO test may be too strict on the indices: they must be orderable (e.g. there's no __lt__ to compare int and str) and hashable. So perhaps test with either all str or all numeric
    @pytest.fixture
    def df1(self):
        '''
        df with in values, and both indices we have: np.nan, float, object, str,
        other and duplicate rows/columns

        Indices and values are not orderable, but they are copyable and a copy equals the original.
        '''
        return pd.DataFrame(
            [
                [np.nan, 5, 5.0, 2.0],
                [5.0, 5, 5, 5],
                [5, 5, 5.0, 5],
                ['str', 5.0, 5, _Object(3)]
            ],
            index=pd.Index((4, 2.0, 2, 'i3'), name='index1'),
            columns=pd.Index((1.0, 5, 1, 'c3'), name='columns1'),
        )

    def assert_(self, df1, df2, expected, **equals_args):
        dfs = [df1, df2]
        dfs_orig = [df.copy() for df in dfs]
        actual = df_.equals(*dfs, _return_reason=True, **equals_args)
        for df, df_orig in zip(dfs, dfs_orig):  # input unchanged
            assert df.equals(df_orig)
            assert df.index.name == df_orig.index.name
            assert df.columns.name == df_orig.columns.name
        assert actual[0] == expected, actual[1]

    def transform_floats(self, df):
        df = df.copy()
        df = self._transform_floats(df)
        df.index = self._transform_floats(df.index)
        df.columns = self._transform_floats(df.columns)
        return df

    def _transform_floats(self, x):
        def transform(x):
            return x+1e-8 if isinstance(x, float) else x
        if isinstance(x, pd.DataFrame):
            return x.applymap(transform)
        if isinstance(x, pd.Index):
            values = x.map(transform)
            return pd.Index(values, name=x.name)
        assert False

    invalid_axi = ({-1}, {2}, {3}, {1.1}, {0,1,2})
    axi = (set(), {0}, {1}, {0,1})

    @pytest.mark.parametrize('value', invalid_axi)
    def test_ignore_order_invalid(self, df1, value):
        '''
        When other value than 0 or 1 in ignore_order, raise ValueError
        '''
        with pytest.raises(ValueError) as ex:
            df_.equals(df1, df1, ignore_order=value)
        assert 'ignore_order' in str(ex.value)
        assert str(value) in str(ex.value)

    @pytest.mark.parametrize('value', invalid_axi)
    def test_ignore_indices_invalid(self, df1, value):
        '''
        When other value than 0 or 1 in ignore_indices, raise ValueError
        '''
        with pytest.raises(ValueError) as ex:
            df_.equals(df1, df1, ignore_indices=value)
        assert 'ignore_indices' in str(ex.value)
        assert str(value) in str(ex.value)

    def test_trivial(self, df1):
        '''
        When equals(df, df), return True

        Even when df contains mix of NaN, object, ... in values and indices, as
        well as duplicates (this also applies to the other tests that expect dfs
        to equal)
        '''
        self.assert_(df1, df1, True)

    def test_return_reason(self, df1):
        '''
        When not return_reason, return only a bool
        '''
        assert df_.equals(df1, df1)

    def test_emptiness(self):
        '''
        When:

        - both empty, return True.
        - either empty, but not both, return False.
        '''
        df = pd.DataFrame([[1]])
        empty = pd.DataFrame()
        self.assert_(df, empty, False)
        self.assert_(empty, df, False)
        self.assert_(empty.copy(), empty, True)

    def test_shape(self):
        '''
        When both non-empty but shape differs, return False
        '''
        self.assert_(pd.DataFrame([[1]]), pd.DataFrame([[1, 2]]), False)
        self.assert_(pd.DataFrame([[1]]), pd.DataFrame([[1], [2]]), False)

    def test_all_close(self, df1):
        '''
        When all_close=True, compare floats in an np.isclose manner
        '''
        df2 = self.transform_floats(df1)
        self.assert_(df1, df2, True, all_close=True)
        self.assert_(df1, df2, False)

    @pytest.mark.parametrize('ignore_indices, change', product(({0}, {1}, {0,1}), ('name', 'values')))
    def test_ignore_indices(self, df1, ignore_indices, change):
        '''
        When ignore_indices, ignore respective index's name and values
        '''
        # create df2
        df2 = df1.copy()
        if 0 in ignore_indices:
            if change == 'name':
                df2.index.name = 'other'
            else:
                df2 = df2.reset_index(drop=True)
        if 1 in ignore_indices:
            if change == 'name':
                df2.columns.name = 'other2'
            else:
                df2.columns = range(len(df2.columns))

        # assert
        self.assert_(df1, df2, True, ignore_indices=ignore_indices)
        self.assert_(df1, df2, False)
        if ignore_indices == {0,1}:
            self.assert_(df1, df2, False, ignore_indices={0})
            self.assert_(df1, df2, False, ignore_indices={1})

    @pytest.mark.parametrize('ignore_order, reorder, all_close', product(
        ({0}, {1}, {0,1}),
        ('index', 'values'),  # whether to reorder the index or the values; the other is set to all 6 so you can no longer tell the difference
        [False, True]  # also test that all_close keeps functioning
    ))
    def test_ignore_order(self, df1, ignore_order, reorder, all_close):
        '''
        When ignore order, ignore a difference in order of tuples of (axis label, axis
        values)

        When not ignoring, detect the difference
        '''
        # create df2
        if all_close:
            df2 = self.transform_floats(df1)
        else:
            df2 = df1.copy()

        # reorder rows/columns
        if 0 in ignore_order:
            df2 = df2.reset_index().reindex([0, 3, 2, 1]).set_index('index1')
        if 1 in ignore_order:
            df2 = df2.transpose().reset_index().reindex([0, 3, 2, 1]).set_index('columns1').transpose()

        # make reordered values or indices indistinguishable
        if reorder == 'values':
            if 0 in ignore_order:
                df1.index = df1.index.putmask([False, True, False, True], 6)
                df2.index = df2.index.putmask([False, True, False, True], 6)
            if 1 in ignore_order:
                df1.columns = df1.columns.putmask([False, True, False, True], 6)
                df2.columns = df2.columns.putmask([False, True, False, True], 6)
        elif reorder == 'index':
            if 0 in ignore_order:
                df1.iloc[[1,3]] = 6
                df2.iloc[[1,3]] = 6
            if 1 in ignore_order:
                df1.iloc[:,[1,3]] = 6
                df2.iloc[:,[1,3]] = 6
        else:
            assert False

        # assert
        self.assert_(df1, df2, True, ignore_order=ignore_order, all_close=all_close)
        self.assert_(df1, df2, False, all_close=all_close)
        if ignore_order == {0,1}:
            self.assert_(df1, df2, False, ignore_order={0}, all_close=all_close)
            self.assert_(df1, df2, False, ignore_order={1}, all_close=all_close)

    @pytest.mark.parametrize('ignore_order, all_close', product(axi, [False, True]))
    def test_nan_equals_none(self, df1, ignore_order, all_close):
        '''
        NaN and None values are considered equal
        '''
        df2 = df1.copy()
        df1.iloc[0,0] = np.nan
        df2.iloc[0,0] = None
        self.assert_(df1, df2, True, ignore_order=ignore_order, all_close=all_close)

class TestAssertEquals(object):

    '''
    Trivial testing that assumes we forward to df_.equals
    '''

    def test_happy_days(self):
        '''
        All args forwarded, raise assert iff not equal
        '''
        df1 = pd.DataFrame(
            [
                [0, 1, 2],
                [3, 4, 5],
                [6, 7, 8]
            ],
            index=['i1', 'i2', 'i3'],
            columns=['c1', 'c2', 'c3']
        )
        df2 = pd.DataFrame(
            [
                [3, 5, 4],
                [0, 2 + 1e-8, 1],
                [6, 8, 7]
            ]
        )
        df_.assert_equals(df1, df2, ignore_order={0,1}, ignore_indices={0,1}, all_close=True)

        with pytest.raises(AssertionError):
            df_.assert_equals(df1, df2, ignore_order={0,1}, all_close=True)
