# Copyright (C) 2017 VIB - Tim Diels <timdiels.m@gmail.com>
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
`setuptools:pkg_resources` extensions.
'''

from pkg_resources import resource_isdir, resource_listdir, resource_stream, resource_filename  # @UnresolvedImport
from pathlib import Path
import shutil

def resource_path(package_or_requirement, resource_name):
    '''
    Like ``resource_filename`` but return a :py:class:`~pathlib.Path` instead.

    Parameters
    ----------
    package_or_requirement : str
    resource_name : str

    Returns
    -------
    ~pathlib.Path
        Path to resource.
    '''
    return Path(resource_filename(package_or_requirement, resource_name))

def resource_copy(package_or_requirement, resource_name, destination):
    '''
    Copy file/dir resource to destination.

    Parameters
    ----------
    package_or_requirement : str
    resource_name : str
    destination : ~pathlib.Path
        Path to copy to, it must not exist.
    '''
    args = package_or_requirement, resource_name
    if resource_isdir(*args):
        destination.mkdir()
        for name in resource_listdir(*args):
            resource_copy(
                package_or_requirement,
                str(Path(resource_name) / name),
                destination / name
            )
    else:
        with destination.open('wb') as f:
            with resource_stream(*args) as source:
                shutil.copyfileobj(source, f)
