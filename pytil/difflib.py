# Copyright (C) 2017 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
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
`python:difflib` extensions.
'''

from more_itertools import sliced
from difflib import ndiff

def line_diff(original, new):
    '''
    :py:obj:`~difflib.ndiff` two (long) lines.

    Breaks up each line in 70 char chunks with tabs replaced by ``→``, ndiffs
    the chunks and returns the diff as a string.

    Parameters
    ----------
    original : str
        Original line.
    new : str
        New line.

    Returns
    -------
    str
        Diff of the given lines
    '''
    return '\n'.join(ndiff(_ndiff_arg(original), _ndiff_arg(new)))

def _ndiff_arg(text):
    '''
    Wrap text for use with ndiff and replace tabs with '→'.

    Notes
    -----
    ndiff treats tabs as a single character, this offsets -- and ++ underlines
    when printed. Replacing with a single unicode character ensures they appear
    in the right spot.
    '''
    text = text.replace('\t', '→')
    return list(sliced(text, 70))
