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
from pkg_resources import resource_filename
import re
import pytest

from pytil.xml_compare import assert_xml_equals


def resource_path(*args):
    # pylint: disable=no-value-for-parameter
    return Path(resource_filename(*args))

def test_assert_xml_equals(temp_dir_cwd):
    'Happy days scenario'
    file1a = resource_path(__name__, 'data/test/assert_xml_equals/file1a.xml')
    file1b = resource_path(__name__, 'data/test/assert_xml_equals/file1b.xml')
    file2 = resource_path(__name__, 'data/test/assert_xml_equals/file2.xml')

    # When equal but formatted differently, with namespaces aliased differently,
    # consider them equal
    assert_xml_equals(file1a, file1b)

    # When a formatting, namespaces are the same, but a value differs, consider them different
    with pytest.raises(AssertionError) as ex:
        assert_xml_equals(file1a, file2)

    patterns = (
        'Actual XML.*/file1a.xml',
        'Expected XML.*/file2.xml',
        "Difference.*text.*'val' != 'val2'",
    )
    msg = ex.value.args[0]
    for pattern in patterns:
        assert re.search(pattern, msg)
