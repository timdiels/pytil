# Copyright (C) 2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
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
Test chicken_turtle_util.path
'''

from chicken_turtle_util import path as path_
from pathlib import Path
import pytest

@pytest.fixture
def path():
    return Path('test')

@pytest.fixture
def contents():
    return 'major contents\nnewlined\n'

@pytest.fixture(autouse=True)
def use_tmp(temp_dir_cwd):
    pass

def test_write(path, contents):
    path_.write(path, contents)
    
    with path.open('r') as f:
        assert f.read() == contents
    
def test_read(path, contents):
    with path.open('w') as f:
        f.write(contents)
    assert path_.read(path) == contents
    
class TestRemove(object):
    
    def test_missing(self, path):
        'When remove missing, ignore'
        path_.remove(path)
        
    def test_file(self, path):
        path.touch()
        path_.remove(path)
        assert not path.exists()
        
    def test_empty_dir(self, path):
        path.mkdir()
        path_.remove(path)
        assert not path.exists()
        
    def test_full_dir(self, path):
        path.mkdir()
        (path / 'child').touch()
        (path / 'subdir').mkdir()
        (path / 'subdir' / 'child child').touch()
        path_.remove(path)
        assert not path.exists()
        