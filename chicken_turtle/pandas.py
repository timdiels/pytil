# Copyright (C) 2015 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
# 
# This file is part of Chicken Turtle.
# 
# Chicken Turtle is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Chicken Turtle is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with Chicken Turtle.  If not, see <http://www.gnu.org/licenses/>.

'''
Helper functions for pandas collections
'''

import pandas as pd
import numpy as np

def fill_na_with_none(df):
    '''
    Fill all NaN in DataFrame with None.
    
    These None values will not be treated as 'missing' by DataFrame, as the dtypes will be set to 'object'
    '''
    df.where(pd.notnull(df), None, inplace=True)
    
# TODO does df.values cost copy time?

# XXX have a count_nan or such added to DataFrame with this implementation
def pd_count_null(x):
    '''
    Parameters
    ----------
    x : pd.DataFrame or pd.Series
    
    Returns
    -------
    int
    '''
    return x.isnull().values.sum()
 
def df_count_null(df): # XXX rm
    return df.isnull().values.sum()

def pd_has_null(x): # XXX rm
    '''
    Parameters
    ----------
    x : pd.DataFrame or pd.Series
    
    Returns
    -------
    bool
    '''
    return x.isnull().values.any()

def df_has_null(df): # XXX rm
    return df.isnull().values.any()

def series_has_duplicates(series):
    return len(np.unique(series.values)) != len(series)

def df_expand_iterable_values(df, columns):
    '''
    Expand repeatably iterable values in given columns along row axis.
    
    Column names are maintained, the index is dropped.
    
    >>> pandas.DataFrame([[1,[1,2],[1]],[1,[1,2],[3,4,5]],[2,[1],[1,2]]], columns='check a b'.split())
       check       a          b
    0      1  [1, 2]        [1]
    1      1  [1, 2]  [3, 4, 5]
    2      2     [1]     [1, 2]
    >>> df_expand_iterable_values(df, ['a', 'b'])
      check  a  b
    0     1  1  1
    1     1  2  1
    2     1  1  3
    3     1  1  4
    4     1  1  5
    5     1  2  3
    6     1  2  4
    7     1  2  5
    8     2  1  1
    9     2  1  2
    
    Parameters
    ----------
    df : pandas.DataFrame
    columns : iterable of str, or str
        Columns (or column) to expand. Their values should be repeatably iterable.
        
    Returns
    -------
    pandas.DataFrame
        Data frame with values in `columns` split to rows
    '''
    #TODO could add option to keep_index by using reset_index and eventually set_index. index names trickery: MultiIndex.names, Index.name. Both can be None. If Index.name can be None in which case it translates to 'index' or if that already exists, it translates to 'level_0'. If MultiIndex.names is None, it translates to level_0,... level_N
    if isinstance(columns, str):
        columns = [columns]
        
    for column in columns:
        expanded = np.repeat(df.values, df[column].apply(len).values, axis=0)
        expanded[:, df.columns.get_loc(column)] = np.concatenate(df[column].tolist())
        df = pd.DataFrame(expanded, columns=df.columns)
    return df

def series_invert(series):
    '''
    Swap index with values of series
    
    When planning to join 2 series, use `pandas.Series.map` instead of swapping.
    
    Parameters
    ----------
    series
        Series to swap on, must have a name
    
    Returns
    -------
    pandas.Series
        Series after swap 
    '''
    df = series.reset_index() #TODO alt is to to_frame and then use som dataframe methods
    df.set_index(series.name, inplace=True)
    return df[df.columns[0]]

