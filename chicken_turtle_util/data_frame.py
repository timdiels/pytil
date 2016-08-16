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
Extensions to `pandas.DataFrame`

.. warning::

   Module contents have only been tested on `DataFrame`\ s with an `Index`,
   `DataFrame`\ s using a `MultiIndex` may not work with this module's
   functions.
'''

import pandas as pd
import numpy as np

def replace_na_with_none(df):
    '''
    Replace ``NaN`` values in `pd.DataFrame` with ``None``
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame whose ``NaN`` values to replace
        
    Returns
    -------
    pd.DataFrame
        `df` with ``NaN`` values replaced by None
        
    Notes
    -----
    Like `DataFrame.fillna`, but replaces ``NaN`` values with ``None``, which
    `DataFrame.fillna` cannot do.
    
    These ``None`` values will not be treated as ``NA`` by DataFrame, as the
    dtypes will be set to ``object``
    '''
    return df.where(pd.notnull(df), None)

def split_array_like(df, columns=None):
    '''
    Split cells with array_like values along row axis.
    
    Column names are maintained. The index is dropped, but this may change in the future.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Data frame ``df[columns]`` should have cell values of type `np.array_like`.
    columns : iterable(str) or str or None
        Columns (or column) whose values to split. If None, `df.columns` is used.
        
    Returns
    -------
    pandas.DataFrame
        Data frame with `array_like` values in ``df[columns]`` split across rows,
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
    
    if columns is None:
        columns = df.columns
    elif isinstance(columns, str):
        columns = [columns]
        
    for column in columns:
        expanded = np.repeat(df.values, df[column].apply(len).values, axis=0)
        expanded[:, df.columns.get_loc(column)] = np.concatenate(df[column].tolist())
        df = pd.DataFrame(expanded, columns=df.columns) # XXX can optimise to outside of loop perhaps
        
    # keep types unchanged
    for i, dtype in enumerate(dtypes):
        df.iloc[:,i] = df.iloc[:,i].astype(dtype)
     
    return df

def equals(df1, df2, ignore_order=set(), ignore_index=False, ignore_columns=False, return_reason=False):
    '''
    Get whether 2 data frames are equal
    
    Parameters
    ----------
    df1, df2 : pd.DataFrame
        Data frames to compare
    ignore_order : {int}
        Axi in which to ignore order
    ignore_index : bool
        If True, ignore index values and name, but unless ``0 in ignore_order``
        still take into account the row order
    ignore_columns : bool
        If True, ignore columns values and name, but unless ``1 in ignore_order``
        still take into account the column order
    return_reason : bool
        If True, `equals` returns a tuple containing the reason, else `equals`
        only returns a bool indicating equality (or equivalence rather)
        
    Returns
    -------
    equal : bool
        Whether they're equal (after ignoring according to the parameters)
    reason : str or None
        If equal, ``None``, otherwise short explanation of why the data frames
        aren't equal. Omitted if not `return_reason`.
    
        
    Examples
    --------
    >>> from chicken_turtle_util import data_frame as df_
    >>> import pandas as pd
    >>> df = pd.DataFrame([
    ...        [1, 2, 3],
    ...        [4, 5, 6],
    ...        [7, 8, 9]
    ...    ],
    ...    index=pd.Index(('i1', 'i2', 'i3'), name='index1'),
    ...    columns=pd.Index(('c1', 'c2', 'c3'), name='columns1')
    ... )
    >>> df
    columns1  c1  c2  c3
    index1              
    i1         1   2   3
    i2         4   5   6
    i3         7   8   9
    >>> df2 = df.reindex(('i3', 'i1', 'i2'), columns=('c2', 'c1', 'c3'))
    >>> df2
    columns1  c2  c1  c3
    index1              
    i3         8   7   9
    i1         2   1   3
    i2         5   4   6
    >>> df_.equals(df, df2)
    False
    >>> df_.equals(df, df2, ignore_order=(0,1))
    True
    >>> df2 = df.copy()
    >>> df2.index = [1,2,3]
    >>> df2
    columns1  c1  c2  c3
    1          1   2   3
    2          4   5   6
    3          7   8   9
    >>> df_.equals(df, df2)
    False
    >>> df_.equals(df, df2, ignore_index=True)
    True
    >>> df2 = df.reindex(('i3', 'i1', 'i2'))
    >>> df2
    columns1  c1  c2  c3
    index1              
    i3         7   8   9
    i1         1   2   3
    i2         4   5   6
    >>> df_.equals(df, df2, ignore_index=True)  # does not ignore row order!
    False
    >>> df_.equals(df, df2, ignore_order={0})
    True
    >>> df2 = df.copy()
    >>> df2.index.name = 'other'
    >>> df_.equals(df, df2)  # df.index.name must match as well, same goes for df.columns.name
    False
    '''
    result = _equals(df1, df2, ignore_order, ignore_index, ignore_columns)
    if return_reason:
        return result
    else:
        return result[0]
    
def _equals(df1, df2, ignore_order=set(), ignore_index=False, ignore_columns=False):
    if ignore_order - {0,1}:
        raise ValueError('invalid ignore_order, valid axi are 0 and 1, got: {!r}'.format(ignore_order))
    
    dfs = [df1.copy(), df2.copy()]
    
    empty_count = sum(df.empty for df in dfs)
    if empty_count == 2:
        return True, None
    if empty_count:
        return False, 'Either empty, but not both'
    
    # If shape differs, never equal
    if df1.shape != df2.shape:
        return False, 'Shape differs'
    
    # Compare index names and reset index
    if ignore_index:
        for df in dfs:
            df.reset_index(drop=True, inplace=True)
    else:
        if dfs[0].index.name != dfs[1].index.name:
            return False, 'Index name differs: {!r} != {!r}'.format(dfs[0].index.name, dfs[1].index.name)
        for df in dfs:
            df.index.name = _unique_element(df.columns)
            df.reset_index(inplace=True)
    
    # Compare columns names and reset columns
    if not ignore_columns:
        if dfs[0].columns.name != dfs[1].columns.name:
            return False, 'Columns name differs: {!r} != {!r}'.format(dfs[0].columns.name, dfs[1].columns.name)
        for df in dfs:
            df.loc[len(df)] = df.columns  # index has already been reset, so len(df) is not in index yet
    for df in dfs:
        df.columns = range(len(df.columns))
    
    # Continue with just the values
    values = np.array([df.values for df in dfs])
    values = np.frompyfunc(lambda x: '({!r})({!r})'.format(x, type(x)), 1, 1)(values)
    
    # If ignore columns, sort columns by values
    if 1 in ignore_order:
        values.sort(axis=2)
    
    # If ignore rows, sort rows by values
    if 0 in ignore_order:
        values.sort(axis=1)
        
    # If values (which may include index and column values) differ, return False
    if not np.array_equal(values[0], values[1]):
        return False, 'Values, index values and/or column values differ:\n{}\n\n{}'.format(values[0], values[1])
    
    return True, None

def _unique_element(index):
    '''
    Get a unique element not yet in the given pd.Index
    
    Deterministic. Inputs with different ordering lead to the same return value.
    '''
    return ''.join(map(str, index.sort_values())) + '_index'
