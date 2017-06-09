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

from chicken_turtle_util.test import assert_text_equals
from contextlib import suppress
from pathlib import Path
import hashlib
import time
import os

#: The file system root to use (used for testing)
_root = Path('/')

def write(path, contents, mode=None): # TODO consider rm in favor of pathlib.Path.write_text and write_bytes. This allows setting mode though...
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

def read(path): #TODO rm in favor of pathlib.Path.read_text and read_bytes
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

def remove(path, force=False):
    '''
    Remove file or directory (recursively), unless it's missing

    On NFS file systems, if a directory contains .nfs* temporary files
    (sometimes created when deleting a file), it waits for them to go away.

    Parameters
    ----------
    path : Path
        Path to remove
    force : bool
        If True, will remove files and directories even if they are read-only
        (as if first doing chmod -R +w)
    '''
    if not path.exists():
        return
    else:
        if force:
            with suppress(FileNotFoundError):
                chmod(path, 0o700, '+', recursive=True)
        if path.is_dir() and not path.is_symlink():
            # Note: shutil.rmtree did not handle NFS well

            # First remove all files
            for dir_, dirs, files in os.walk(str(path), topdown=False): # bottom-up walk
                dir_ = Path(dir_)
                for file in files:
                    with suppress(FileNotFoundError):
                        (dir_ / file).unlink()
                for file in dirs:  # Note: os.walk treats symlinks to directories as directories
                    file = dir_ / file
                    if file.is_symlink():
                        with suppress(FileNotFoundError):
                            file.unlink()

            # Now remove all dirs, being careful of any lingering .nfs* files
            for dir_, _, _ in os.walk(str(path), topdown=False): # bottom-up walk
                dir_ = Path(dir_)
                with suppress(FileNotFoundError):
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
            with suppress(FileNotFoundError):
                path.unlink()

def chmod(path, mode, operator='=', recursive=False):
    '''
    Change file mode bits

    When recursively chmodding a directory, executable bits in `mode` are
    ignored when applying to a regular file. E.g. ``chmod(path, mode=0o777,
    recursive=True)`` would apply ``mode=0o666`` to regular files.

    Symlinks are ignored.

    Parameters
    ----------
    path : Path
        Path to chmod
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
    if path.is_symlink():
        # Do not chmod or follow symlinks
        return
    path.chmod(mode_)

    # then its children
    def chmod_children(parent, files, mode_mask, operator):
        for file in files:
            with suppress(FileNotFoundError):
                file = parent / file
                if not file.is_symlink():
                    chmod(file, mode & mode_mask, operator)
    if recursive and path.is_dir():
        for parent, dirs, files in os.walk(str(path)):
            parent = Path(parent)
            chmod_children(parent, dirs, 0o777777, operator)
            chmod_children(parent, files, 0o777666, operator)

# Note: good delete and copy here, but pb paths which we won't expose: https://plumbum.readthedocs.org/en/latest/utils.html

def hash(path, hash_function=hashlib.sha512):
    '''
    Hash file or directory

    Parameters
    ----------
    path : pathlib.Path
        File or directory to hash
    hash_function : () -> hash
        Function which returns hashlib hash objects

    Returns
    -------
    hash
        hashlib hash object of file/directory contents. File/directory stat data
        is ignored. The directory digest covers file/directory contents and
        their location relative to the directory being digested. The directory
        name itself is ignored.
    '''
    hash_ = hash_function()
    if path.is_dir():
        for directory, directories, files in os.walk(str(path), topdown=True):
            # Note:
            # - directory: path to current directory in walk relative to current working direcotry
            # - directories/files: dir/file names

            # Note: file names can contain nearly any character (even newlines).

            # hash like (ignore the whitespace):
            #
            #   h(relative-dir-path)
            #   h(dir_name)
            #   h(dir_name2)
            #   ,
            #   h(file_name) h(file_content)
            #   h(file_name2) h(file_content2)
            #   ;
            #   h(relative-dir-path2)
            #   ...
            hash_.update(hash_function(str(Path(directory).relative_to(path)).encode()).digest())
            for name in sorted(directories):
                hash_.update(hash_function(name.encode()).digest())
            hash_.update(b',')
            for name in sorted(files):
                hash_.update(hash_function(name.encode()).digest())
                hash_.update(hash(Path(directory) / name).digest())
            hash_.update(b';')
    else:
        with path.open('rb') as f:
            while True:
                buffer = f.read(65536)
                if not buffer:
                    break
                hash_.update(buffer)
    return hash_

def assert_mode(path, mode):
    '''
    Assert last 3 octal mode digits match given mode exactly

    Parameters
    ----------
    path : pathlib.Path
        Path whose mode to assert
    mode : int
        Expected mode
    '''
    actual = path.stat().st_mode & 0o777
    assert actual == mode, '{:o} != {:o}'.format(actual, mode)

def assert_equals(file1, file2, contents=True, name=True, mode=True):
    '''
    Assert 2 files are equal

    Parameters
    -----------
    file1 : Path
    file2 : Path
    contents : bool
        Assert file contents are equal
    name : bool
        Assert file names are equal
    mode : bool
        Assert the last 3 octal digits of file modes are equal 
    '''
    if name:
        assert file1.name == file2.name
    if contents:
        assert_text_equals(read(file1), read(file2))
    if mode:
        assert file1.stat().st_mode == file2.stat().st_mode
