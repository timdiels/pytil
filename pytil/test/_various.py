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

from formencode.doctest_xml_compare import xml_compare
from contextlib import contextmanager
from itertools import zip_longest
from more_itertools import ilen
from pathlib import Path
from pytil import path as path_  # yay, 'resolving' circular dependencies
from pytil.difflib import line_diff
from pytil.path import sorted_lines
from lxml import etree  # @UnresolvedImport
import logging
import pytest
import os
import re

@pytest.yield_fixture()
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

    #
    os.chdir(str(original_cwd))

def reset_loggers(name, root=True):
    '''
    Reset loggers matching name pattern.

    .. warning::

       :py:func:`reset_loggers` is incompatible with
       :py:func:`~logging.basicConfig` as the latter cannot be reset. E.g. if a
       first test uses :py:func:`~logging.basicConfig`, a call to it in a next
       test will be ignored as it could not be reset.

    Parameters
    ----------
    name : str
        Reset only loggers whose name match this regex pattern. This does not
        include the root logger, see the ``root`` param.
    root : bool
        Reset the root logger iff `True`.

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
    Assert long strings are equal.

    Parameters
    ----------
    actual : str
    expected : str
    '''
    assert_lines_equal(actual.splitlines(), expected.splitlines())

def assert_text_contains(whole, part):
    '''
    Assert long string contains given string.

    Parameters
    ----------
    whole : str
    part : str
    '''
    assert part in whole, '\nActual:\n{}\n\nExpected to contain:\n{}'.format(whole, part)

def assert_matches(actual, pattern, flags=0):
    '''
    Assert string matches pattern.

    Parameters
    ----------
    actual : str
    pattern : str
    flags : int
        Regex flags.
    '''
    assert re.match(pattern, actual, flags), 'Actual:\n{}\n\nExpected to match:\n{}'.format(actual, pattern)

def assert_search_matches(actual, pattern, flags=0):
    '''
    Assert string matches pattern by search.

    Parameters
    ----------
    actual : str
    pattern : str
    flags : int
        Regex flags.
    '''
    assert re.search(pattern, actual, flags), 'Actual:\n{}\n\nExpected a subset to match:\n{}'.format(actual, pattern)

def assert_lines_equal(actual, expected):
    '''
    Assert (long) lines equal.

    Reports first line that differs, in detail.

    Parameters
    ----------
    actual : ~typing.Iterable[str]
        Actual lines.
    expected : ~typing.Iterable[str]
        Expected lines.
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
    Assert long line equals.

    Parameters
    ----------
    actual : str
        Actual line.
    expected : str
        Expected line.
    i : int
        Line index (if coming from a collection of lines), for prettier output.
    '''
    if actual != expected:
        diff = line_diff(actual, expected)
        assert False, 'Line {} (0-based) differs (-actual, +expected) :\n{}'.format(i, diff)

def assert_xml_equals(actual, expected):
    '''
    Assert xml files/strings are equivalent.

    Differences in formatting or attribute order are ignored. Comments are
    ignored as well. Differences in element order are significant though!

    Parameters
    ----------
    actual : ~typing.BinaryIO or ~pathlib.Path or str
        Actual XML, as file object or Path to XML file, or XML contents as
        string.
    expected : ~typing.BinaryIO or ~pathlib.Path or str
        Expected XML, as file object or Path to XML file, or XML contents as
        string.
    '''
    # Note: if this ever breaks, there is a way to write out XML to file
    # canonicalised. StringIO may help in not having to use any temp files
    # http://lxml.de/api/lxml.etree._ElementTree-class.html#write_c14n
    def tree(xml):
        if isinstance(xml, str):
            xml = etree.fromstring(str(xml))
        else:
            if isinstance(xml, Path):
                xml = str(xml)
            xml = etree.parse(xml)
        return xml.getroot()
    def raise_assert(msg):
        assert False, 'XMLs differ\n\nActual XML:\n{!r}\n\nExpected XML:\n{!r}\n\nDifference: {}'.format(actual, expected, msg)
    xml_compare(tree(actual), tree(expected), reporter=raise_assert)

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
    assert actual == expected, '\nActual: {}\nExpected: {}'.format(actual, expected)

# TODO probably need a more flexible way of doing this, e.g. some need to
# compared as csv, some have a header, some don't, some as tsv, some just txt,
# xml even, ...
def assert_dir_equals(actual_dir, expected_dir, expected_files_count):
    # Assert expected dir is set up correctly
    assert \
        ilen(expected_dir.iterdir()) == expected_files_count, \
        'Some expected files are missing'

    # Assert expected files match those in actual dir
    for expected_file in expected_dir.iterdir():
        if expected_file.suffix == '.log':
            continue
        print(expected_file.name)
        actual_file = actual_dir / expected_file.name
        assert_lines_equal(sorted_lines(actual_file), sorted_lines(expected_file))

    # Assert actual dir has no additional files, ignoring log files
    def children(dir_):
        children = {child.name for child in dir_.iterdir()}
        return {child for child in children if not child.endswith('.log')}
    actual = children(actual_dir)
    expected = children(expected_dir)
    assert actual == expected, '\nActual {}\nExpected {}'.format(actual, expected)

def assert_file_mode(path, mode):
    '''
    Assert last 3 octal mode digits match given mode exactly.

    Parameters
    ----------
    path : ~pathlib.Path
        Path whose mode to assert.
    mode : int
        Expected mode.
    '''
    actual = path.stat().st_mode & 0o777
    assert actual == mode, '{:o} != {:o}'.format(actual, mode)

def assert_file_equals(actual_file, expected_file, contents=True, name=True, mode=True):
    '''
    Assert 2 files are equal.

    Parameters
    -----------
    actual_file : ~pathlib.Path
    expected_file : ~pathlib.Path
    contents : bool
        Assert file contents are equal.
    name : bool
        Assert file names are equal.
    mode : bool
        Assert the last 3 octal digits of file modes are equal.
    '''
    if name:
        assert actual_file.name == expected_file.name
    if contents:
        assert_text_equals(actual_file.read_text(), expected_file.read_text())
    if mode:
        assert actual_file.stat().st_mode == expected_file.stat().st_mode
