# Copyright (C) 2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
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
Test utilities.
'''

from itertools import zip_longest
from pathlib import Path
import logging
import pytest
import os
import re

@pytest.yield_fixture()
def temp_dir_cwd(tmpdir):
    '''
    pytest fixture that sets current working directory to a temporary directory
    '''
    original_cwd = Path.cwd()
    os.chdir(str(tmpdir))
    yield tmpdir

    # ensure the user has full permissions on temp dir (so that pytest can remove it later)
    path_.chmod(Path(str(tmpdir)), 0o700, '+', recursive=True)

    #
    os.chdir(str(original_cwd))

def reset_loggers(name, root=True):
    '''
    Reset loggers matching name pattern

    ``logging.basicConfig`` cannot be reset, so subsequent calls to it will be
    ignored as usual.

    Parameters
    ----------
    name : str
        Reset only loggers whose name match this regex pattern. This does not
        include the root logger, see the ``root`` param.
    root : bool
        Reset the root logger iff True.

    Examples
    --------
    To reset your loggers and the root logger before each test::

        @pytest.fixture(autouse=True)
        def global_auto():
            reset_loggers('mypkg(\..*)?')
    '''
    pattern = re.compile(name)

    # Reset root logger
    # Note: it is not included in loggerDict
    # Note: logging.getLogger(root_logger.name) != root_logger
    if root:
        _reset_logger(logging.getLogger())

    # Reset other loggers
    for name, logger in logging.Logger.manager.loggerDict.items():  # @UndefinedVariable
        if isinstance(logger, logging.Logger) and pattern.fullmatch(name):
            _reset_logger(logger)

def _reset_logger(logger):
    # Remove handlers and filters
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    for filter_ in logger.filters[:]:
        logger.removeFilter(filter_)

def assert_text_equals(actual, expected):
    '''
    Assert long strings are equal
    '''
    assert actual == expected, '\nActual:\n{}\n\nExpected:\n{}'.format(actual, expected)

def assert_text_contains(whole, part):
    '''
    Assert long string contains given string
    '''
    assert part in whole, '\nActual:\n{}\n\nExpected to contain:\n{}'.format(whole, part)

def assert_matches(actual, pattern, flags=0):
    assert re.match(pattern, actual, flags), 'Actual:{}\n\nExpected to match:\n{}'.format(actual, pattern)

def assert_search_matches(actual, pattern, flags=0):
    assert re.search(pattern, actual, flags), 'Actual:{}\n\nExpected a subset to match:\n{}'.format(actual, pattern)

def assert_lines_equal(actual, expected):
    '''
    Assert (long) lines equal

    Reports first line that differs, in detail.

    Parameters
    ----------
    actual : iterable(str)
    expected : iterable(str)
    '''
    # Note: the for loop is much faster than a single assert
    line_pairs = zip_longest(actual, expected)
    unequal_counts_msg = (
        'There are {} lines than expected, '
        'or there is a None value in {} lines'
    )
    for i, (actual_line, expected_line) in enumerate(line_pairs):
        assert actual_line is not None, unequal_counts_msg.format('fewer', 'actual')
        assert expected_line is not None, unequal_counts_msg.format('more', 'expected')
        _assert_line_equals(actual_line, expected_line, i)

def _assert_line_equals(actual, expected, i):
    '''
    Assert long line equals

    Parameters
    ----------
    actual : str
    expected : str
    i : int
        Line index (if coming from a collection of lines)
    '''
    if actual != expected:
        diff = line_diff(actual, expected)
        assert False, 'Line {} (0-based) differs (-actual, +expected) :\n{}'.format(i, diff)

from pytil.difflib import line_diff
from pytil import path as path_  # yay, 'resolving' circular dependencies
