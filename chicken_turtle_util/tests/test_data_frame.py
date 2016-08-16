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
Test chicken_turtle_util.data_frame 
'''

import chicken_turtle_util.data_frame as df_
from chicken_turtle_util.data_frame import replace_na_with_none, split_array_like
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

class EqualsTestCases(object):
    
    def _get_expected(self, emptiness, transformed1_args, transformed2_args, equals_args):
        # When both empty, always equal
        if all(emptiness):
            return True
        
        # When one empty, never equal
        if any(emptiness):
            return False
        
        # When equals(df, df, ...), return True
        if not any(transformed2_args.values()):
            return True
        
        # When a row/column dropped, return False
        if transformed2_args['drop_row'] or transformed2_args['drop_column']:
            return False
        
        # When types differ, return False
        if transformed2_args['string_values']:
            return False
        
        # ignore order iff relevant axis in ignore_order
        if transformed2_args['reorder_index'] and 0 not in equals_args['ignore_order']:
            # and can notice the reordering
            index_order_differs = not equals_args['ignore_index'] and not transformed1_args['single_valued_index']
            values_order_differs = not transformed1_args['single_valued']
            if index_order_differs or values_order_differs:
                return False
        if transformed2_args['reorder_columns'] and 1 not in equals_args['ignore_order']:
            # and can notice the reordering
            columns_order_differs = not equals_args['ignore_columns'] and not transformed1_args['single_valued_columns']
            values_order_differs = not transformed1_args['single_valued']
            if columns_order_differs or values_order_differs:
                return False
        
        # only ignore index values and name iff ignore_index
        if transformed2_args['reset_index'] and not equals_args['ignore_index']:
            return False
        
        # only ignore columns values and name iff ignore_columns
        if transformed2_args['reset_columns'] and not equals_args['ignore_columns']:
            return False
        
        # else, return True
        return True
    
    #TODO add NaN handling, default nan!=nan, but add option which treat nan==nan. Also nan in indices
    def cases(self):
        '''
        All possible inputs and outputs for df1
        '''
        bools = [True, False]
        ignore_orders = [set(), {0}, {1}, {0,1}]
        for emptiness in product(bools, bools):  # if left: use empty df, else use df1; if right: use empty df, else use df2 
            for equals_args in product(ignore_orders, bools, bools):
                equals_args = dict(zip(['ignore_order', 'ignore_index', 'ignore_columns'], equals_args))
                equals_args['return_reason'] = True
                if not any(emptiness):
                    for transformed1_args in product(*([bools] * 3)):
                        transformed1_args = dict(zip(['single_valued', 'single_valued_index', 'single_valued_columns'], transformed1_args))
                        for transformed2_args in product(*([bools] * 7)):
                            transformed2_args = dict(zip(['reset_index', 'reset_columns', 'reorder_index', 'reorder_columns', 'string_values', 'drop_row', 'drop_column'], transformed2_args))
                            expected = self._get_expected(emptiness, transformed1_args, transformed2_args, equals_args)
                            yield emptiness, transformed1_args, transformed2_args, equals_args, expected
                else:
                    expected = self._get_expected(emptiness, None, None, equals_args)
                    yield emptiness, None, None, equals_args, expected
    
class TestEquals(object):
    
    @pytest.fixture
    def df1(self):
        return pd.DataFrame(
            [
                [1, 6, 7, 4],
                [5, 6, 7, 8],
                [5, 6, 7, 8],
                [9, 6, 7, 12]
            ],
            index=pd.Index(('i1', 'i2', 'i3', 'i3'), name='index1'),
            columns=pd.Index(('c1', 'c2', 'c3', 'c3'), name='columns1')
        )
        
    def transformed1(self, df, single_valued, single_valued_index, single_valued_columns):
        df = df.copy()
        if single_valued:
            df = pd.DataFrame(np.ones_like(df.values), index=df.index, columns=df.columns)
        if single_valued_index:
            df.index = pd.Index(np.ones_like(df.index.values), name=df.index.name)
        if single_valued_columns:
            df.columns = pd.Index(np.ones_like(df.columns.values), name=df.columns.name)
        return df
        
    def transformed2(self, df, reset_index, reset_columns, reorder_index, reorder_columns, string_values, drop_row, drop_column):
        # Note: `df` should be a 4x4
        df = df.copy()
        if reorder_index:
            df = df.reset_index().reindex((2, 0, 1, 3)).set_index('index1')
        if reorder_columns:
            df = df.transpose().reset_index().reindex((1, 2, 0, 3)).set_index('columns1').transpose()
        if reset_index:
            df = df.reset_index(drop=True)
        if reset_columns:
            df.columns = range(len(df.columns))
        if string_values:
            df = df.applymap(str)
        if drop_row:
            df = df.iloc[[0, 1, 3]]
        if drop_column:
            df = df.iloc[:,[0,1,3]]
        return df
        
    @pytest.mark.parametrize('value', ({-1}, {2}, {3}, {1.1}, {0,1,2}))
    def test_ignore_order_invalid(self, df1, value):
        '''
        When other value than 0 or 1 in ignore_order, raise ValueError
        '''
        with pytest.raises(ValueError) as ex:
            df_.equals(df1, df1, ignore_order=value)
        assert 'ignore_order' in str(ex.value)
        assert str(value) in str(ex.value)
        
    @pytest.mark.parametrize('emptiness, transformed1_args, transformed2_args, equals_args, expected', EqualsTestCases().cases())
    def test_other(self, df1, emptiness, transformed1_args, transformed2_args, equals_args, expected):
        if any(emptiness):
            if emptiness[1]:
                df2 = pd.DataFrame()
            else:
                df2 = df1
            if emptiness[0]:
                df1 = pd.DataFrame()
        else:
            df1 = self.transformed1(df1, **transformed1_args)
            df2 = self.transformed2(df1, **transformed2_args)
        df1_orig = df1.copy()
        df2_orig = df2.copy()
        actual = df_.equals(df1, df2, **equals_args)
        assert df1.equals(df1_orig)
        assert df1.index.name == df1_orig.index.name
        assert df1.columns.name == df1_orig.columns.name
        assert df2.equals(df2_orig)
        assert df2.index.name == df2_orig.index.name
        assert df2.columns.name == df2_orig.columns.name
        assert actual[0] == expected, actual[1]
    
    def test_return_reason(self, df1):
        '''
        When not return_reason, return only a bool
        '''
        assert df_.equals(df1, df1)

# TODO
'''
XXX test with MultiIndex indices. Then remove warning from data_frame
'''