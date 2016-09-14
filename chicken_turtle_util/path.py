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
Extensions to pathlib.
'''

from pathlib import Path
import time
import os
import hashlib

#: The file system root to use (used for testing)
_root = Path('/')

def write(path, contents, mode=None):
    '''
    Create or overwrite file with contents
    
    Missing parent directories of `path` will be created.
    
    Parameters
    ----------
    path : pathlib.Path
        Path to file to write to
    contents : str
        Contents to write to file
    mode : int or None
        If set, also chmod file
    '''
    os.makedirs(str(path.parent), exist_ok=True)
    path.touch()
    if mode is not None:
        path.chmod(0o600)
    with path.open('w') as f:
        f.write(contents)
    if mode is not None:
        path.chmod(mode)
        
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
    
    On NFS file systems, if a directory contains .nfs* temporary files
    (sometimes created when deleting a file), it waits for them to go away.
    
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
            # Note: shutil.rmtree did not handle NFS well
            
            # First remove all files
            for dir_, _, files in os.walk(str(path), topdown=False): # bottom-up walk
                for file in files:
                    (Path(dir_) / file).unlink()
                    
            # Now remove all dirs, being careful of any lingering .nfs* files
            for dir_, _, _ in os.walk(str(path), topdown=False): # bottom-up walk
                dir_ = Path(dir_)
                
                # wait for .nfs* files
                children = list(dir_.iterdir())
                while children:
                    # only wait for nfs temporary files
                    if any(not child.name.startswith('.nfs') for child in children):
                        dir_.rmdir()  # raises dir not empty
                        
                    # wait and go again
                    time.sleep(.1)
                    children = list(dir_.iterdir())
                
                # rm
                dir_.rmdir()
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
            dir_ = Path(dir_)
            for child in dirs:
                chmod((dir_ / child), mode, operator)
            for file in files:
                chmod((dir_ / file), mode & 0o777666, operator)
        
# Note: good delete and copy here, but pb paths which we won't expose: https://plumbum.readthedocs.org/en/latest/utils.html

def digest(path):
    '''
    Get SHA512 checksum of file or directory
     
    Parameters
    ----------
    path : pathlib.Path
        file or directory to hash
     
    Returns
    -------
    type_of(hashlib.sha512)
        hash object of file/directory contents. File/directory stat data is
        ignored. The directory digest covers file/directory contents and their
        location relative to the directory being digested. The directory name
        itself is ignored.
    '''
    hash_ = hashlib.sha512()
    if path.is_dir():
        for directory, directories, files in os.walk(str(path), topdown=True):
            # Note:
            # - directory: path to current directory in walk relative to current working direcotry
            # - directories/files: dir/file names
            
            # hash like:
            #
            #   relative-dir-path
            #   (
            #       (dir_name)
            #       (dir_name2)
            #   )
            #   (
            #       (file_name)(file_hash)
            #       (file_name2)(file_hash2)
            #   )
            #   relative-dir-path2
            #   ...
            hash_.update(str(Path(directory).relative_to(path)).encode())
            hash_.update(b'(')
            for name in sorted(directories):
                hash_.update(b'(' + name.encode() + b')')
            hash_.update(b')(')
            for name in sorted(files):
                hash_.update(b'(' + name.encode() + b')')
                hash_.update(b'(' + digest(Path(directory) / name).digest() + b')')
            hash_.update(b')')
    else:
        with path.open('rb') as f:
            while True:
                buffer = f.read(65536)
                if not buffer:
                    break
                hash_.update(buffer)
    return hash_
