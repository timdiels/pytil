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

#TODO there is no guarantee that inplace=True offers better performance, stop using it unless it's actually handy http://stackoverflow.com/questions/22532302/pandas-peculiar-performance-drop-for-inplace-rename-after-dropna

import pandas as pd
import numpy as np
import logging
ma = np.ma

logger = logging.getLogger(__name__)

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

# Note: if want to optimise further, could try: http://stackoverflow.com/questions/17116814/pandas-how-do-i-split-text-in-a-column-into-multiple-rows/17116976#17116976
# Would be nice to have a generic way of splitting. I.e. by func (value -> parts)
#TODO maintain the index (and columns as we already do, should be docced)
#TODO also compare performance to trivial implementation: split=pd.concat(df.reset_index().[col].apply(pd.Series)); del df[col]; df=df.join(split) 
def split_array_like(df, columns=None): #TODO rename TODO if it's not a big performance hit, just make them arraylike? We already indicated the column explicitly (sort of) so...
    '''
    Split cells with array_like values along row axis.

    Column names are maintained. The index is dropped, but this may change in the future.

    Parameters
    ----------
    df : pd.DataFrame
        Data frame ``df[columns]`` should have cell values of type `np.array_like`.
    columns : iterable(str) or str or None
        Columns (or column) whose values to split. If None, `df.columns` is used.

    Returns
    -------
    pd.DataFrame
        Data frame with `array_like` values in ``df[columns]`` split across rows,
        and corresponding values in other columns repeated.

    Examples
    --------
    >>> df = pd.DataFrame([[1,[1,2],[1]],[1,[1,2],[3,4,5]],[2,[1],[1,2]]], columns=('check', 'a', 'b'))
    >>> df
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

    for column in columns: #TODO pulling apart and working with values, ... constructing one new df at the end may be faster and use less memory
        expanded = np.repeat(df.values, df[column].apply(len).values, axis=0)
        expanded[:, df.columns.get_loc(column)] = np.concatenate(df[column].tolist())
        df = pd.DataFrame(expanded, columns=df.columns) # XXX can optimise to outside of loop perhaps

    # keep types unchanged
    for i, dtype in enumerate(dtypes):
        df.iloc[:,i] = df.iloc[:,i].astype(dtype)

    return df

def equals(df1, df2, ignore_order=set(), ignore_indices=set(), all_close=False, _return_reason=False):
    '''
    Get whether 2 data frames are equal

    ``NaN``\ s are considered equal (which is consistent with
    `pandas.DataFrame.equals`). ``None`` is considered equal to ``NaN``.

    Parameters
    ----------
    df1, df2 : pd.DataFrame
        Data frames to compare
    ignore_order : {int}
        Axi in which to ignore order
    ignore_indices : {int}
        Axi of which to ignore the index. E.g. ``{1}`` allows differences in
        ``df.columns.name`` and `df.columns.equals(df2.columns)``.
    all_close : bool
        If False, values must match exactly, if True, floats are compared as if
        compared with `np.isclose`.
    _return_reason : bool
        Internal. If True, `equals` returns a tuple containing the reason, else
        `equals` only returns a bool indicating equality (or equivalence
        rather).

    Returns
    -------
    equal : bool
        Whether they're equal (after ignoring according to the parameters)
    reason : str or None
        If equal, ``None``, otherwise short explanation of why the data frames
        aren't equal. Omitted if not `_return_reason`.

    Notes
    -----
    All values (including those of indices) must be copyable and `__eq__` must
    be such that a copy must equal its original. A value must equal itself
    unless it's `np.nan`. Values needn't be orderable or hashable (however
    pandas requires index values to be orderable and hashable). By consequence,
    this is not an efficient function, but it is flexible.

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
    >>> df_.equals(df, df2, ignore_indices={0})
    True
    >>> df2 = df.reindex(('i3', 'i1', 'i2'))
    >>> df2
    columns1  c1  c2  c3
    index1              
    i3         7   8   9
    i1         1   2   3
    i2         4   5   6
    >>> df_.equals(df, df2, ignore_indices={0})  # does not ignore row order!
    False
    >>> df_.equals(df, df2, ignore_order={0})
    True
    >>> df2 = df.copy()
    >>> df2.index.name = 'other'
    >>> df_.equals(df, df2)  # df.index.name must match as well, same goes for df.columns.name
    False
    '''
    result = _equals(df1, df2, ignore_order, ignore_indices, all_close)
    if _return_reason:
        return result
    else:
        return result[0]

def _equals(df1, df2, ignore_order, ignore_indices, all_close):
    if ignore_order - {0,1}:
        raise ValueError('invalid ignore_order, valid axi are 0 and 1, got: {!r}'.format(ignore_order))

    if ignore_indices - {0,1}:
        raise ValueError('invalid ignore_indices, valid axi are 0 and 1, got: {!r}'.format(ignore_indices))

    dfs = [df1.copy(), df2.copy()]

    # If both empty, return True right away
    if dfs[0].empty and dfs[1].empty:
        return True, None

    # If shape differs, never equal
    if dfs[0].shape != dfs[1].shape:
        return False, 'Shape differs'

    # Compare index and columns names
    if 0 not in ignore_indices:
        if dfs[0].index.name != dfs[1].index.name:
            return False, 'Index name differs: {!r} != {!r}'.format(dfs[0].index.name, dfs[1].index.name)
    if 1 not in ignore_indices:
        if dfs[0].columns.name != dfs[1].columns.name:
            return False, 'Columns name differs: {!r} != {!r}'.format(dfs[0].columns.name, dfs[1].columns.name)

    # Add non-ignored indices to values
    arrays = []
    for df in dfs:
        values = df.values
        if 1 not in ignore_indices:
            values = np.vstack([df.columns.values, values])
        if 0 not in ignore_indices:
            index_values = df.index.values
            if 1 not in ignore_indices:
                index_values = np.hstack([np.nan, index_values])
            values = np.column_stack([index_values, values])
        arrays.append(values)

    # Compare just the values
    if not _2d_array_equals(arrays, ignore_order, all_close):
        return False, 'Either of df.index, df.columns, df.values differ'

    return True, None

def _2d_array_equals(arrays, ignore_order, all_close):
    #XXX can further optimise by using better numpy routines Maybe able to optimise at an algorithmic level first though
    # e.g. nditer has more efficient ways. There's also Cython of course
    if not ignore_order:
        for value1, value2 in zip(*[values.ravel() for values in arrays]):
            if not _value_equals(value1, value2, all_close=all_close):
                return False
    else:
        # Compare along each axis 
        for axis in (0, 1):
            if axis not in ignore_order:
                continue # only check along the other axis

            values1 = arrays[0]
            values2 = arrays[1]
            if axis == 1:
                values1 = values1.transpose()
                values2 = values2.transpose()
            values1 = np.require(values1, requirements='C')
            values2 = ma.asarray(values2, order='C')

            # Note: c-contiguous stores in memory as: row 1, row 2, ...
            for row1 in values1:
                if not _try_mask_first_row(row1, values2, all_close, len(ignore_order) == 2):
                    return False
    return True

def _try_mask_first_row(row, values, all_close, ignore_order):
    '''
    mask first row in 2d array

    values : 2d masked array
        Each row is either fully masked or not masked at all
    ignore_order : bool
        Ignore column order

    Return whether masked a row. If False, masked nothing.
    '''
    for row2 in values:
        mask = ma.getmaskarray(row2)
        assert mask.sum() in (0, len(mask))  # sanity check: all or none masked
        if mask[0]: # Note: at this point row2's mask is either all False or all True
            continue

        # mask each value of row1 in row2
        if _try_mask_row(row, row2, all_close, ignore_order):
            return True
    # row did not match
    return False

def _try_mask_row(row1, row2, all_close, ignore_order):
    '''
    if each value in row1 matches a value in row2, mask row2

    row1
        1d array
    row2
        1d masked array whose mask is all False
    ignore_order : bool
        Ignore column order
    all_close : bool
        compare with np.isclose instead of ==

    Return whether masked the row
    '''
    if ignore_order:
        for value1 in row1:
            if not _try_mask_first_value(value1, row2, all_close):
                row2.mask = ma.nomask
                return False
    else:
        for value1, value2 in zip(row1, row2):
            if not _value_equals(value1, value2, all_close):
                return False
        row2[:] = ma.masked
    assert row2.mask.all()  # sanity check
    return True

def _try_mask_first_value(value, row, all_close):
    '''
    mask first value in row

    value1 : any
    row : 1d masked array
    all_close : bool
        compare with np.isclose instead of ==

    Return whether masked a value
    '''
    # Compare value to row
    for i, value2 in enumerate(row):
        if _value_equals(value, value2, all_close):
            row[i] = ma.masked
            return True
    return False

def _value_equals(value1, value2, all_close):
    '''
    Get whether 2 values are equal

    value1, value2 : any
    all_close : bool
        compare with np.isclose instead of ==
    '''
    if value1 is None:
        value1 = np.nan
    if value2 is None:
        value2 = np.nan

    are_floats = np.can_cast(type(value1), float) and np.can_cast(type(value2), float)
    if all_close and are_floats:
        return np.isclose(value1, value2, equal_nan=True)
    else:
        if are_floats:
            return value1 == value2 or (value1 != value1 and value2 != value2)
        else:
            return value1 == value2

def assert_equals(df1, df2, ignore_order=set(), ignore_indices=set(), all_close=False, _return_reason=False):
    '''
    Assert 2 data frames are equal

    Like ``assert equals(df1, df2, ...)``, but with better hints at where the
    data frames differ. See :func:`chicken_turtle_util.data_frame.equals` for
    detailed parameter doc.

    Parameters
    ----------
    df1, df2 : pd.DataFrame
    ignore_order : {int}
    ignore_indices : {int}
    all_close : bool
    '''
    equals_, reason = equals(df1, df2, ignore_order, ignore_indices, all_close, _return_reason=True)
    assert equals_, '{}\n\n{}\n\n{}'.format(reason, df1.to_string(), df2.to_string())
