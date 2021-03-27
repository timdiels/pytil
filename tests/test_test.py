# Copyright (C) 2016-2021 VIB/BEG/UGent - Tim Diels <tim@diels.me>
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

from pathlib import Path
from textwrap import dedent

import pytest

from pytil.test import assert_dir_unchanged


def test_assert_dir_unchanged(temp_dir_cwd):
    dir_ = Path('dir')
    dir_.mkdir()

    # When dir unchanged, nothing happens
    with assert_dir_unchanged(dir_):
        pass

    # When dir does change, raise
    with pytest.raises(AssertionError) as ex:
        with assert_dir_unchanged(dir_):
            (dir_ / 'child').mkdir()
    assert ex.value.args[0] == dedent('''
        Actual: {'dir/child'}
        Expected: set()'''
    )
