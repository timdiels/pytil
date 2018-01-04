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
Test pytil.pkg_resources
'''

from pytil.pkg_resources import resource_path, resource_copy
from pytil.test import assert_file_equals
from pathlib import Path

def test_resource_copy(temp_dir_cwd):  # @UnusedVariable
    '''
    Test resource_copy, happy days
    '''
    # Copy dir recursively
    actual_dir = Path('destination')
    resource = 'data/pkg_resources/resource_copy'
    expected_dir = resource_path(__name__, resource)
    resource_copy(__name__, resource, actual_dir)

    # Assert actual == expected
    for file in ('file', 'subdir/file1', 'subdir/file2'):
        assert_file_equals(actual_dir / file, expected_dir / file)
