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
import shutil
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
    
def remove(path):
    '''
    Remove file or directory (recursively), unless it's missing
    
    Parameters
    ----------
    path : Path
        path to remove
    '''
    if not path.exists():
        return
    elif path.is_dir():
        shutil.rmtree(str(path))
    else:
        path.unlink()
        
# Note: good delete and copy here, but pb paths which we won't expose: https://plumbum.readthedocs.org/en/latest/utils.html

# Finish adding when needed: docstring is done. If implement properly, remove the note. Test it.
# # https://github.com/cakepietoast/checksumdir/blob/master/checksumdir/__init__.py
# # license: https://github.com/cakepietoast/checksumdir/blob/master/LICENSE.txt
# # dependency: checksumdir
# from checksumdir import dirhash
# old = dirhash(str(path), 'sha512')
# import hashlib
# def digest(path):
#     '''
#     Get SHA512 checksum of file or directory
#     
#     See `checksumdir.dirhash` on how a directory's hash is calculated.
#     
#     .. note::
#     
#         The current implementation does not yet take into account the relative
#         path (including file names) of files in a directory when hashing a
#         directory.
#     
#     Parameters
#     ----------
#     path : pathlib.Path
#         file or directory to hash
#     
#     Returns
#     -------
#     bytes
#         digest of file or directory contents. If a directory, the digest takes
#         into account the file contents of each of its descendants combined with
#         their relative path, the directory name itself is ignored. File stat
#         data is ignored.
#     '''
#     with path.open('rb') as f:
#         hash_ = hashlib.sha512()
#         while True:
#             buffer = f.read(65536)
#             hash_.update(buffer)
#             if not buffer:
#                 return hash_.digest()
            