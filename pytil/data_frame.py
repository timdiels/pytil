# Copyright (C) 2015 VIB/BEG/UGent - Tim Diels <tim@diels.me>
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

r'''
`pandas.DataFrame` extensions.

.. warning::

   Module contents have only been tested on :py:class:`~pandas.DataFrame`\ s
   with an :py:class:`~pandas.Index`, :py:class:`~pandas.DataFrame`\ s using a
   :py:class:`~pandas.MultiIndex` may not work with this module's functions.
'''

import numpy as np
import logging
ma = np.ma

# TODO there is no guarantee that inplace=True offers better performance, stop
# using it unless it's actually handy
# http://stackoverflow.com/questions/22532302/pandas-peculiar-performance-drop-for-inplace-rename-after-dropna


def df_equals(df1, df2, ignore_order=frozenset(), ignore_indices=frozenset(),
                                        all_close=False, _return_reason=False):
    '''
    Get whether 2 data frames are equal.

    ``NaN`` is considered equal to ``NaN`` and `None`.

    Parameters
    ----------
    df1 : ~pandas.DataFrame
        Data frame to compare.
    df2 : ~pandas.DataFrame
        Data frame to compare.
    ignore_order : ~typing.Set[int]
        Axi in which to ignore order.
    ignore_indices : ~typing.Set[int]
        Axi of which to ignore the index. E.g. ``{1}`` allows differences in
        ``df.columns.name`` and does not check
        ``df.columns.equals(df2.columns)``.
    all_close : bool
        If `False`, values must match exactly, if `True`, floats are compared as if
        compared with `numpy.isclose`.
    _return_reason : bool
        Internal. If `True`, `equals` returns a tuple containing the reason, else
        `equals` only returns a bool indicating equality (or equivalence
        rather).

    Returns
    -------
    bool
        Whether they are equal (after ignoring according to the parameters).

        Internal note: if ``_return_reason``, ``Tuple[bool, str or None]`` is
        returned. The former is whether they're equal, the latter is `None` if
        equal or a short explanation of why the data frames aren't equal,
        otherwise.

    Notes
    -----
    All values (including those of indices) must be copyable and ``__eq__`` must
    be such that a copy must equal its original. A value must equal itself
    unless it's ``NaN``. Values needn't be orderable or hashable (however
    pandas requires index values to be orderable and hashable). By consequence,
    this is not an efficient function, but it is flexible.

    Examples
    --------
    >>> from pytil import data_frame as df_
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
    # pylint: disable=too-many-branches
    if ignore_order - {0,1}:
        raise ValueError(
            f'invalid ignore_order, valid axi are 0 and 1, got: {ignore_order!r}'
        )

    if ignore_indices - {0,1}:
        raise ValueError(
            f'invalid ignore_indices, valid axi are 0 and 1, got: {ignore_indices!r}'
        )

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
            return False, (
                f'Index name differs: {dfs[0].index.name!r} != {dfs[1].index.name!r}'
            )
    if 1 not in ignore_indices:
        if dfs[0].columns.name != dfs[1].columns.name:
            return False, (
                f'Columns name differs: {dfs[0].columns.name!r} != {dfs[1].columns.name!r}'
            )

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

    value1 : ~typing.Any
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

    value1, value2 : ~typing.Any
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
            return value1 == value2 or (np.isnan(value1) and np.isnan(value2))
        else:
            return value1 == value2

def assert_df_equals(df1, df2, ignore_order=frozenset(),
                     ignore_indices=frozenset(), all_close=False,
                     _return_reason=False):
    '''
    Assert 2 data frames are equal

    A more verbose form of ``assert equals(df1, df2, ...)``. See `equals` for
    an explanation of the parameters.

    Parameters
    ----------
    df1 : ~pandas.DataFrame
        Actual data frame.
    df2 : ~pandas.DataFrame
        Expected data frame.
    ignore_order : ~typing.Set[int]
    ignore_indices : ~typing.Set[int]
    all_close : bool
    '''
    equals_, reason = df_equals(
        df1, df2, ignore_order, ignore_indices, all_close, _return_reason=True
    )
    assert equals_, f'{reason}\n\n{df1.to_string()}\n\n{df2.to_string()}'
