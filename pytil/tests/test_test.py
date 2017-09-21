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
    assert_matches, assert_search_matches
)
from pathlib import Path
from textwrap import dedent
import logging
import pytest

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
