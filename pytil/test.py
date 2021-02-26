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


from contextlib import contextmanager
from pathlib import Path
from pytil import path as path_  # yay, 'resolving' circular dependencies
import pytest
import os


# Used by cedalion
@pytest.fixture
def temp_dir_cwd(tmpdir):
    '''
    pytest fixture which sets current working directory to a temporary
    directory.
    '''
    original_cwd = Path.cwd()
    os.chdir(str(tmpdir))
    yield tmpdir

    # ensure the user has full permissions on temp dir (so that pytest can remove it later)
    path_.chmod(Path(str(tmpdir)), 0o700, '+', recursive=True)

    os.chdir(str(original_cwd))

# Used by cedalion
@contextmanager
def assert_dir_unchanged(path, ignore=()):
    '''
    Assert dir unchanged after code block.

    Parameters
    ----------
    path : ~pathlib.Path
        Dir to assert for changes.
    ignore : ~typing.Collection[~pathlib.Path]
        Paths to ignore in comparison.

    Examples
    --------
    >>> with assert_dir_unchanged(Path('input')):
    ...    Path('input/child').mkdir()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AssertionError: ...
    '''
    def contents():
        children = set(path.iterdir())
        ignored_children = {
            child
            for child in children
            for path in ignore
            if path_.is_descendant_or_self(child, path)
        }
        return set(map(str, children - ignored_children))
    expected = contents()
    yield
    actual = contents()
    assert actual == expected, f'\nActual: {actual}\nExpected: {expected}'
