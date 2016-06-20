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
Test utilities. Contains `temp_dir_cwd`, pytest fixture that cd's to temporary directory
'''

import pytest
import os
from pathlib import Path
from chicken_turtle_util import path as path_

@pytest.yield_fixture()
def temp_dir_cwd(tmpdir):
    '''
    pytest fixture that sets current working directory to a temporary directory
    '''
    original_cwd = Path.cwd()
    os.chdir(str(tmpdir))
    yield tmpdir
    
    # ensure the user has full permissions on temp dir (so that pytest can remove it later)
    path_.chmod(Path(str(tmpdir)), 0o700, '+', recursive=True)
    
    #
    os.chdir(str(original_cwd))