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

from formencode.doctest_xml_compare import xml_compare
from lxml import etree


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
        assert False, (
            f'XMLs differ\n'
            f'Actual XML: {actual}\n'
            f'Expected XML: {expected}\n'
            f'Difference: {msg}'
        )
    xml_compare(tree(actual), tree(expected), reporter=raise_assert)
