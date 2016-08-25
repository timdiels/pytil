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

def equals(df1, df2, ignore_order=set(), ignore_index=False, ignore_columns=False, all_close=False, return_reason=False):
    '''
    Get whether 2 data frames are equal
    
    ``NaN``\ s are considered equal, which is analog to `pandas.DataFrame.equals`.
    
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
    all_close : bool
        If False, values must match exactly, if True, floats are compared as if
        compared with `np.isclose`.
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
    result = _equals(df1, df2, ignore_order, ignore_index, ignore_columns, all_close)
    if return_reason:
        return result
    else:
        return result[0]
    
def _array_equal(arr1, arr2, equal_nan=False):
    if equal_nan:
        return ((arr1 == arr2) | ((arr1 != arr1) & (arr2 != arr2))).all()
    else:
        return np.array_equal(arr1, arr2)

#TODO refactor by axis
def _equals(df1, df2, ignore_order, ignore_index, ignore_columns, all_close): #TODO test all_close
    if ignore_order - {0,1}:
        raise ValueError('invalid ignore_order, valid axi are 0 and 1, got: {!r}'.format(ignore_order))
    
    dfs = [df1.copy(), df2.copy()]
    
    empty_count = sum(df.empty for df in dfs)
    if empty_count == 2:
        return True, None
    if empty_count:
        return False, 'Either empty, but not both'
    
    # If shape differs, never equal
    if dfs[0].shape != dfs[1].shape:
        return False, 'Shape differs'
    
    # If dtypes differ, never equal
    if (dfs[0].dtypes != dfs[1].dtypes).any():
        return False, 'dtypes differ: {!r} != {!r}'.format(dfs[0].dtypes, dfs[1].dtypes)
    
    # Compare index and columns names
    if not ignore_index:
        if dfs[0].index.name != dfs[1].index.name:
            return False, 'Index name differs: {!r} != {!r}'.format(dfs[0].index.name, dfs[1].index.name)
    if not ignore_columns:
        if dfs[0].columns.name != dfs[1].columns.name:
            return False, 'Columns name differs: {!r} != {!r}'.format(dfs[0].columns.name, dfs[1].columns.name)
    
    #
    for i, df in enumerate(dfs):
        # If row order ignored, sort rows by values
        if 0 in ignore_order:
            _ignore_row_order(df, not ignore_index)
                
        # If column order ignored, sort columns by values
        if 1 in ignore_order:
            df = df.transpose()
            _ignore_row_order(df, not ignore_columns)
            df = df.transpose()
            dfs[i] = df
        
        # If index / columns ignored, reset respectively
        if ignore_index:
            df.reset_index(drop=True, inplace=True)
        if ignore_columns:
            df.columns = range(len(df.columns))
    
    # Compare index values of both axi
    for axis_name, ignore, indices in [('Index', ignore_index, [df.index for df in dfs]), ('Columns', ignore_columns, [df.columns for df in dfs])]:
        if ignore:
            continue
        if all_close and all(index.dtype == float for index in indices):
            equal = np.allclose(indices[0].values, indices[1].values, equal_nan=True)
        else:
            equal = indices[0].equals(indices[1])
        if not equal:
            return False, '{} values differ'.format(axis_name)
    
    # Compare values: floats
    values = [df.values for df in dfs]
    is_float = np.frompyfunc(lambda x: isinstance(x, float), 1, 1)
    float_values = [vals[is_float(vals).astype(bool)] for vals in values]
    if all_close:
        equal = np.allclose(*float_values, equal_nan=True)
    else:
        equal = _array_equal(*float_values, equal_nan=True)
    if not equal:
        return False, 'Float values differ:\n{}\n\n{}'.format(*float_values)
     
    # Compare values: other
    other_values = [vals[~is_float(vals).astype(bool)] for vals in values]
    if not (other_values[0] == other_values[1]).all():
        return False, 'Non-float values differ:\n{}\n\n{}'.format(*other_values)
    
    return True, None

def _ignore_row_order(df, include_index):
    columns = df.columns
    df.columns = range(len(columns)) # reset columns as sort_values needs unique column labels
    if include_index:
        index_name = object()  # a unique name, object() only equals itself
        df.index.name = index_name
        df.reset_index(inplace=True)
    df.sort_values(by=df.columns.tolist(), inplace=True)
    if include_index:
        df.set_index(index_name, inplace=True)
    df.columns = columns
