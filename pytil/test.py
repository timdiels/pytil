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

import pytest
import os
import re
from pathlib import Path

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

from pytil import path as path_  # yay, 'resolving' circular dependencies
