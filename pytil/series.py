# Copyright (C) 2016 VIB/BEG/UGent - Tim Diels <tim@diels.me>
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

'`pandas.Series` extensions'

from pytil.data_frame import df_equals


def invert(series):
    '''
    Swap index with values of series.

    Parameters
    ----------
    series : ~pandas.Series
        Series to swap on, must have a name.

    Returns
    -------
    ~pandas.Series
        Series after swap.

    See also
    --------
    pandas.Series.map
        Joins series ``a -> b`` and ``b -> c`` into ``a -> c``.
    '''
    df = series.reset_index() #TODO alt is to to_frame and then use som dataframe methods
    df.set_index(series.name, inplace=True)
    return df[df.columns[0]]

def equals(series1, series2, ignore_order=False, ignore_index=False,
                             all_close=False, _return_reason=False):
    '''
    Get whether 2 series are equal.

    ``NaN`` is considered equal to ``NaN`` and `None`.

    Parameters
    ----------
    series1 : pandas.Series
        Series to compare.
    series2 : pandas.Series
        Series to compare.
    ignore_order : bool
        Ignore order of values (and index).
    ignore_index : bool
        Ignore index values and name.
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
        equal or a short explanation of why the series aren't equal, otherwise.

    Notes
    -----
    All values (including those of indices) must be copyable and ``__eq__`` must
    be such that a copy must equal its original. A value must equal itself
    unless it's ``NaN``. Values needn't be orderable or hashable (however
    pandas requires index values to be orderable and hashable). By consequence,
    this is not an efficient function, but it is flexible.
    '''
    result = _equals(series1, series2, ignore_order, ignore_index, all_close)
    if _return_reason:
        return result
    else:
        return result[0]

def _equals(series1, series2, ignore_order, ignore_index, all_close):
    if not ignore_index:
        if series1.name != series2.name:
            return False, f'Series name differs: {series1.name!r} != {series2.name!r}'
    return df_equals(
        series1.to_frame(),
        series2.to_frame(),
        ignore_order={0} if ignore_order else set(),
        ignore_indices={0} if ignore_index else set(),
        all_close=all_close,
        _return_reason=True
    )

# Used by cedalion
def assert_equals(actual, expected, ignore_order=False, ignore_index=False, all_close=False):
    '''
    Assert 2 series are equal.

    Like ``assert equals(series1, series2, ...)``, but with better hints at
    where the series differ. See `equals` for
    detailed parameter doc.

    Parameters
    ----------
    actual : ~pandas.Series
    expected : ~pandas.Series
    ignore_order : bool
    ignore_index : bool
    all_close : bool
    '''
    equals_, reason = equals(
        actual, expected, ignore_order, ignore_index, all_close, _return_reason=True
    )
    assert equals_, f'{reason}\n\n{actual.to_string()}\n\n{expected.to_string()}'
