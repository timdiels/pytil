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
Utilities for working with `pandas.DataFrame`
'''

import pandas as pd
import numpy as np

def replace_na_with_none(df):
    '''
    Replace NaN values in DataFrame with None
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame whose NaN values to replace
        
    Returns
    -------
    pd.DataFrame
        `df` with NaN values replaced by None
        
    Notes
    -----
    Like `DataFrame.fillna`, but replaces NaN values with None, which
    `DataFrame.fillna` cannot do.
    
    These None values will not be treated as 'missing' by DataFrame, as the
    dtypes will be set to 'object'
    '''
    return df.where(pd.notnull(df), None)

def split_array_like(df, columns):
    '''
    Split cells with array_like values along row axis.
    
    Column names are maintained. The index is dropped, but this may change in the future.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Data frame `df[columns]` should have cell values of type `np.array_like`.
    columns : iterable(str) or str
        Columns (or column) whose values to split.
        
    Returns
    -------
    pandas.DataFrame
        Data frame with `array_like` values in `df[columns]` split across rows,
        and corresponding values in other columns repeated.
        
    Examples
    --------
    >>> pandas.DataFrame([[1,[1,2],[1]],[1,[1,2],[3,4,5]],[2,[1],[1,2]]], columns=('check', 'a', 'b'))
       check       a          b
    0      1  [1, 2]        [1]
    1      1  [1, 2]  [3, 4, 5]
    2      2     [1]     [1, 2]
    >>> split_array_like(df, ['a', 'b'])
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
    '''
    #TODO could add option to keep_index by using reset_index and eventually set_index. index names trickery: MultiIndex.names, Index.name. Both can be None. If Index.name can be None in which case it translates to 'index' or if that already exists, it translates to 'level_0'. If MultiIndex.names is None, it translates to level_0,... level_N
    dtypes = df.dtypes
    
    if isinstance(columns, str):
        columns = [columns]
        
    for column in columns:
        expanded = np.repeat(df.values, df[column].apply(len).values, axis=0)
        expanded[:, df.columns.get_loc(column)] = np.concatenate(df[column].tolist())
        df = pd.DataFrame(expanded, columns=df.columns) # XXX can optimise to outside of loop perhaps
        
    # keep types unchanged
    for i, dtype in enumerate(dtypes):
        df.iloc[:,i] = df.iloc[:,i].astype(dtype)
     
    return df

