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
Test pytil.test
'''

from pytil.pkg_resources import resource_path
from pytil.test import (
    reset_loggers, assert_dir_unchanged, assert_text_equals, assert_xml_equals,
    assert_matches, assert_file_equals
)
from pathlib import Path
from textwrap import dedent
import logging
import pytest

@pytest.fixture(autouse=True)
def use_tmp(temp_dir_cwd):
    pass

def test_reset_loggers():
    '''
    When loggers have been messed with, reset resets them to a fresh state
    '''
    logger_names = (None, 'pytil.test.unusedmodulename')
    loggers = list(map(logging.getLogger, logger_names))

    # Mess with loggers
    for logger in loggers:
        logger.addHandler(logging.StreamHandler())
        logger.addFilter(logging.Filter())

    # Reset
    reset_loggers('pytil\.test\.unusedmodule.*')

    # Assert loggers have been reset
    for logger in loggers:
        assert not logger.handlers
        assert not logger.filters

def test_assert_dir_unchanged(temp_dir_cwd):  # @UnusedVariable
    '''
    Test test.assert_dir_unchanged
    '''
    dir_ = Path('dir')
    dir_.mkdir()

    # When dir unchanged, nothing happens
    with assert_dir_unchanged(dir_):
        pass

    # When dir does change, raise
    with pytest.raises(AssertionError) as ex:
        with assert_dir_unchanged(dir_):
            (dir_ / 'child').mkdir()
    assert_text_equals(ex.value.args[0], dedent('''
            Actual: {'dir/child'}
            Expected: set()'''
        )
    )

def test_assert_xml_equals(temp_dir_cwd):  # @UnusedVariable
    '''
    Test assert_xml_equals, simple happy days
    '''
    file1a = resource_path(__name__, 'data/test/assert_xml_equals/file1a.xml')
    file1b = resource_path(__name__, 'data/test/assert_xml_equals/file1b.xml')
    file2 = resource_path(__name__, 'data/test/assert_xml_equals/file2.xml')

    # When equal but formatted differently, with namespaces aliased differently,
    # consider them equal
    assert_xml_equals(file1a, file1b)

    # When a formatting, namespaces are the same, but a value differs, consider them different
    with pytest.raises(AssertionError) as ex:
        assert_xml_equals(file1a, file2)
    assert_matches(ex.value.args[0], dedent('''\
            XMLs differ
            
            Actual XML:
            PosixPath\('.*/file1a.xml'\)
            
            Expected XML:
            PosixPath\('.*/file2.xml'\)
            
            Difference: text: 'val' != 'val2\''''
        )
    )

class TestAssertFileEquals(object):

    def test_contents(self):
        '''
        Only when contents=True, assert file contents match  
        '''
        file1 = Path('file1')
        file2 = Path('file2')
        contents = 'abc'
        file1.write_text(contents)
        file2.write_text(contents*2)
        assert_file_equals(file1, file2, name=False, contents=False, mode=False)
        with pytest.raises(AssertionError):
            assert_file_equals(file1, file2, contents=True, name=False, mode=False)
        file2.write_text(contents)
        assert_file_equals(file1, file2, contents=True, name=False, mode=False)

    def test_name(self):
        '''
        When name=True, assert file names match  
        '''
        Path('dir1').mkdir()
        Path('dir2').mkdir()
        file1a = Path('dir1/file_a')
        file2a = Path('dir2/file_a')
        file2b = Path('dir2/file_b')
        file1a.touch()
        file2a.touch()
        file2b.touch()
        assert_file_equals(file1a, file2b, name=False, contents=False, mode=False)
        with pytest.raises(AssertionError):
            assert_file_equals(file1a, file2b, name=True, contents=False, mode=False)
        assert_file_equals(file1a, file2a, name=True, contents=False, mode=False)

    def test_mode(self):
        '''
        When mode=True, assert file modes match  
        '''
        file1 = Path('file1')
        file2 = Path('file2')
        mode = 0o754
        file1.touch(mode)
        file2.touch(0o666)
        assert_file_equals(file1, file2, name=False, contents=False, mode=False)
        with pytest.raises(AssertionError):
            assert_file_equals(file1, file2, mode=True, name=False, contents=False)
        file2.chmod(mode)
        assert_file_equals(file1, file2, mode=True, name=False, contents=False)
