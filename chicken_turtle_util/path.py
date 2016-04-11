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
Path utilities
'''

from pathlib import Path 
import os

#: The file system root to use (used for testing)
_root = Path('/')

def write(path, contents):
    '''
    Create or overwrite file with contents
    
    Missing parent directories of `path` will be created.
    
    Parameters
    ----------
    path : pathlib.Path
        Path to file to write to
    contents : str
        Contents to write to file
    '''
    os.makedirs(str(path.parent), exist_ok=True)
    with path.open('w') as f:
        f.write(contents)
        
def read(path):
    '''
    Get file contents
    
    Parameters
    ----------
    path : pathlib.Path
        Path of file to read
        
    Returns
    -------
    str
        File contents
    '''
    with path.open('r') as f:
        return f.read()