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
Test pytil.http
'''

import pytest
from pytil.http import download
from pytil.test import temp_dir_cwd
from pathlib import Path

class TestDownload(object):

    file_name_headers = [('Content-Disposition', 'attachment; filename="lorem_ipsum.txt"')]
    params = (
        ('.', (), 'unknown', None),
        ('.', file_name_headers,'lorem_ipsum.txt', 'lorem_ipsum.txt'), 
        ('existing_file', file_name_headers, 'existing_file', 'lorem_ipsum.txt'), 
        ('new_file', file_name_headers, 'new_file', 'lorem_ipsum.txt')
    )

    @pytest.mark.parametrize('destination, headers, path_expected, name_expected', params)
    def test_download(self, temp_dir_cwd, destination, headers, path_expected, name_expected, httpserver):
        '''
        Test all of `download`

        - When destination is directory, README.md is saved in it
        - When destination is a file, it is overwritten with README.md contents
        - When destination does not exist, it is overwritten with README.md contents
        '''
        httpserver.serve_content(lorem_ipsum, headers=headers)
        path_expected = Path(path_expected)
        destination = Path(destination)
        Path('existing_file').write_text('exists')
        path, name = download(httpserver.url, destination)
        assert path == path_expected
        assert path.exists()
        assert name == name_expected
        with path_expected.open() as f:
            assert f.read() == lorem_ipsum

lorem_ipsum = '''
Bacon ipsum dolor amet flank pastrami tenderloin, meatball pork belly shank biltong bresaola. Ball tip ham jowl corned beef turkey shankle. Leberkas boudin andouille jerky, tenderloin corned beef filet mignon venison sirloin jowl t-bone. Cupim flank venison meatloaf, swine chuck pork loin alcatra pig drumstick pork belly salami frankfurter hamburger picanha. Venison ribeye kielbasa leberkas beef ribs meatball. Bacon prosciutto picanha, flank shankle pork chop chuck pancetta swine tongue biltong. Doner leberkas turkey, pork pastrami kevin pancetta.
''' * 1000
