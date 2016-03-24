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
Test chicken_turtle_util.algorithms
'''

import pytest
from chicken_turtle_util.data_frame import replace_na_with_none, split_array_like
import pandas as pd
import numpy as np

class ReplaceNAWithNone(object):

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
      
    def test_not_inplace(self, df, df_replaced):
        '''When df contains NaN and inplace=False, df contains NaN, return has NaN replaced'''
        df_original = df.copy()
        retval = replace_na_with_none(df)
        assert df.equals(df_original)
        assert retval.equals(df_replaced)
      
    def test_inplace(self, df, df_replaced):
        '''When df contains NaN and inplace=True, df and return have NaN replaced'''
        retval = replace_na_with_none(df, inplace=True)
        assert df.equals(df_replaced)
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
        result = split_array_like(df, ('a', 'b'))
        assert split_array_like(df, ('a', 'b')).equals(df_split_a_b) # Note: test should allow index to differ
        assert split_array_like(df, iter(('a', 'b'))).equals(df_split_a_b)
    
    def test_split_a(self, df, df_split_a):
        '''When split on 'a', correct split'''
        assert split_array_like(df, 'a').equals(df_split_a)
        assert split_array_like(df, ('a',)).equals(df_split_a)
        