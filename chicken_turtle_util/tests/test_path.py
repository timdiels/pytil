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
from contextlib import contextmanager
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
        
class TestChmod(object):
    
    @pytest.fixture
    def root(self):
        root = Path('root_dir')
        root.mkdir()
        return root
    
    @pytest.fixture
    def child_dir(self, root):
        child = root / 'child_dir'
        child.mkdir()
        return child
    
    @pytest.fixture
    def child_file(self, root):
        child = root / 'child_file'
        child.touch()
        return child
    
    @pytest.fixture
    def grand_child(self, child_dir):
        child = child_dir / 'grand_child'
        child.touch()
        return child
    
    @contextmanager
    def unchanged(self, *paths):
        paths = {path: path.stat().st_mode for path in paths}
        yield
        paths_new = {path: path.stat().st_mode for path in paths}
        assert paths == paths_new
        
    def assert_mode(self, path, mode):
        actual = path.stat().st_mode & 0o777
        assert actual == mode, '{:o} != {:o}'.format(actual, mode)

    @pytest.mark.parametrize('recursive', (False, True))
    def test_file_assign(self, path, recursive):
        path.touch()
        path_.chmod(path, mode=0o777, recursive=recursive)
        self.assert_mode(path, 0o777)
        path_.chmod(path, mode=0o751, recursive=recursive)
        self.assert_mode(path, 0o751)
    
    @pytest.mark.parametrize('recursive', (False, True))    
    def test_file_add(self, path, recursive):
        path.touch()
        path.chmod(0o000)
        path_.chmod(path, 0o111, '+', recursive=recursive)
        self.assert_mode(path, 0o111)
        path_.chmod(path, 0o100, '+', recursive=recursive)
        self.assert_mode(path, 0o111)
        path_.chmod(path, 0o751, '+', recursive=recursive)
        self.assert_mode(path, 0o751)
        
    @pytest.mark.parametrize('recursive', (False, True))
    def test_file_subtract(self, path, recursive):
        path.touch()
        path.chmod(0o777)
        path_.chmod(path, 0o111, '-', recursive=recursive)
        self.assert_mode(path, 0o666)
        path_.chmod(path, 0o751, '-', recursive=recursive)
        self.assert_mode(path, 0o026)
        
    def test_dir_assign(self, root, child_dir, child_file, grand_child):
        with self.unchanged(child_dir, child_file, grand_child):
            path_.chmod(root, mode=0o777)
            self.assert_mode(root, 0o777)
            path_.chmod(root, mode=0o751)
            self.assert_mode(root, 0o751)
            
    def test_dir_add(self, root, child_dir, child_file, grand_child):
        with self.unchanged(child_dir, child_file, grand_child):
            root.chmod(0o000)
            path_.chmod(root, 0o111, '+')
            self.assert_mode(root, 0o111)
            path_.chmod(root, 0o100, '+')
            self.assert_mode(root, 0o111)
            path_.chmod(root, 0o751, '+')
            self.assert_mode(root, 0o751)
            
    def test_dir_subtract(self, root, child_dir, child_file, grand_child):
        with self.unchanged(child_dir, child_file, grand_child):
            root.chmod(mode=0o777)
            path_.chmod(root, 0o011, '-')
            self.assert_mode(root, 0o766)
            path_.chmod(root, 0o271, '-')
            self.assert_mode(root, 0o506)
            
    def test_dir_assign_recursive(self, root, child_dir, child_file, grand_child):
        path_.chmod(root, mode=0o777, recursive=True)
        self.assert_mode(root, 0o777)
        self.assert_mode(child_dir, 0o777)
        self.assert_mode(child_file, 0o666)
        self.assert_mode(grand_child, 0o666)
        
        path_.chmod(root, mode=0o751, recursive=True)
        self.assert_mode(root, 0o751)
        self.assert_mode(child_dir, 0o751)
        self.assert_mode(child_file, 0o640)
        self.assert_mode(grand_child, 0o640)
            
    def test_dir_add_recursive(self, root, child_dir, child_file, grand_child):
        grand_child.chmod(0o000)
        child_dir.chmod(0o000)
        child_file.chmod(0o000)
        root.chmod(0o000)
        
        path_.chmod(root, 0o511, '+', recursive=True)
        self.assert_mode(root, 0o511)
        self.assert_mode(child_dir, 0o511)
        self.assert_mode(child_file, 0o400)
        self.assert_mode(grand_child, 0o400)
        
        path_.chmod(root, 0o500, '+', recursive=True)
        self.assert_mode(root, 0o511)
        self.assert_mode(child_dir, 0o511)
        self.assert_mode(child_file, 0o400)
        self.assert_mode(grand_child, 0o400)
        
        path_.chmod(root, 0o751, '+', recursive=True)
        self.assert_mode(root, 0o751)
        self.assert_mode(child_dir, 0o751)
        self.assert_mode(child_file, 0o640)
        self.assert_mode(grand_child, 0o640)
            
    def test_dir_subtract_recursive(self, root, child_dir, child_file, grand_child):
        root.chmod(mode=0o777)
        child_dir.chmod(0o777)
        child_file.chmod(0o777)
        grand_child.chmod(0o777)
        
        path_.chmod(root, 0o222, '-', recursive=True)
        self.assert_mode(root, 0o555)
        self.assert_mode(child_dir, 0o555)
        self.assert_mode(child_file, 0o555)
        self.assert_mode(grand_child, 0o555)
        
        path_.chmod(root, 0o047, '-', recursive=True)
        self.assert_mode(root, 0o510)
        self.assert_mode(child_dir, 0o510)
        self.assert_mode(child_file, 0o511)
        self.assert_mode(grand_child, 0o511)
            
