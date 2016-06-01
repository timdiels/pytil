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
    
def remove(path, force=False): #TODO test the force
    '''
    Remove file or directory (recursively), unless it's missing
    
    Parameters
    ----------
    path : Path
        path to remove
    force : bool
        If True, will remove read-only files and directories (as if first doing chmod +w)
    '''
    if not path.exists():
        return
    else:
        if force:
            chmod(path, 0o700, '+', recursive=True)
        if path.is_dir():
            shutil.rmtree(str(path))
        else:
            path.unlink()
        
def chmod(path, mode, operator='=', recursive=False):
    '''
    Change file mode bits
    
    When recursively chmodding a directory, executable bits in `mode` are
    ignored when applying to a regular file. E.g. ``chmod(path, mode=0o777,
    recursive=True)`` would apply ``mode=0o666`` to regular files.
    
    Parameters
    ----------
    path : Path
        path to chmod
    mode : int
        Mode bits to apply, e.g. ``0o777``.
    operator : '+' or '-' or '='
        How to apply the mode bits to the file. If '=', assign mode, if '+', add to current
        mode, if '-', subtract from current mode.
    recursive : bool
        Whether to chmod recursively. If recursive, applies modes in a top-down
        fashion, like the chmod command.
    '''
    if mode > 0o777 and operator != '=':
        raise ValueError('Special bits (i.e. >0o777) only supported when using "=" operator')
    
    # first chmod path
    if operator == '+':
        mode_ = path.stat().st_mode | mode
    elif operator == '-':
        mode_ = path.stat().st_mode & ~mode
    else:
        mode_ = mode
    path.chmod(mode_)
    
    # then its children
    if recursive and path.is_dir():
        for dir_, dirs, files in os.walk(str(path)):
            print(dir_, files)
            dir_ = Path(dir_)
            for child in dirs:
                chmod((dir_ / child), mode, operator)
            for file in files:
                chmod((dir_ / file), mode & 0o777666, operator)
        
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
            