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
`python:pathlib` extensions.
'''

from contextlib import suppress, contextmanager
from pathlib import Path
import tempfile
import hashlib
import errno
import time
import os

#: The file system root to use (used for testing)
_root = Path('/')

def remove(path, force=False):
    '''
    Remove file or directory (recursively), if it exists.

    On NFS file systems, if a directory contains :file:`.nfs*` temporary files
    (sometimes created when deleting a file), it waits for them to go away.

    Parameters
    ----------
    path : ~pathlib.Path
        Path to remove.
    force : bool
        If True, will remove files and directories even if they are read-only
        (as if first doing ``chmod -R +w``).
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
    Change file mode bits.

    When recursively chmodding a directory, executable bits in ``mode`` are
    ignored when applying to a regular file. E.g. ``chmod(path, mode=0o777,
    recursive=True)`` would apply ``mode=0o666`` to regular files.

    Symlinks are ignored.

    Parameters
    ----------
    path : ~pathlib.Path
        Path to chmod.
    mode : int
        Mode bits to apply, e.g. ``0o777``.
    operator : str
        How to apply the mode bits to the file, one of:

        '='
            Replace mode with given mode.
        '+'
            Add to current mode.
        '-'
            Subtract from current mode.

    recursive : bool
        Whether to chmod recursively.
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

@contextmanager
def TemporaryDirectory(suffix=None, prefix=None, dir=None, on_error='ignore'):  # @ReservedAssignment
    '''
    An extension to `tempfile.TemporaryDirectory`.

    Unlike with `python:tempfile`, a :py:class:`~pathlib.Path` is yielded on
    ``__enter__``, not a `str`.

    Parameters
    ----------
    suffix : str
        See `tempfile.TemporaryDirectory`.
    prefix : str
        See `tempfile.TemporaryDirectory`.
    dir : ~pathlib.Path
        See `tempfile.TemporaryDirectory`, but pass a :py:class:`~pathlib.Path` instead.
    on_error : str
        Handling of failure to delete directory (happens frequently on NFS), one of:

        raise
            Raise exception on failure.
        ignore
            Fail silently.
    '''
    if dir:
        dir = str(dir)  # @ReservedAssignment
    temp_dir = tempfile.TemporaryDirectory(suffix, prefix, dir)
    try:
        yield Path(temp_dir.name)
    finally:
        try:
            temp_dir.cleanup()
        except OSError as ex:
            print(ex)
            # Suppress relevant errors if ignoring failed delete
            if on_error != 'ignore' or ex.errno != errno.ENOTEMPTY:
                raise

# Note: good delete and copy here, but pb paths which we won't expose: https://plumbum.readthedocs.org/en/latest/utils.html

def hash(path, hash_function=hashlib.sha512):  # @ReservedAssignment
    '''
    Hash file or directory.

    Parameters
    ----------
    path : ~pathlib.Path
        File or directory to hash.
    hash_function : ~typing.Callable[[], hash object]
        Function which creates a hashlib hash object when called. Defaults to
        ``hashlib.sha512``.

    Returns
    -------
    hash object
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

def sorted_lines(file):
    '''
    Lines of file, sorted.

    Parameters
    ----------
    file : ~pathlib.Path
        Path to file whose lines to read.

    Returns
    -------
    ~typing.List[str]
        Sorted lines of file.
    '''
    return sorted(file.read_text().splitlines())

def is_descendant(descendant, ancestor):
    '''
    Get whether path is descendant of other path.

    Uses the absolute path, so symlinks, ... do not affect this.

    Parameters
    ----------
    descendant : ~pathlib.Path
        Supposed descendant.
    ancestor : ~pathlib.Path
        Supposed ancestor.

    Returns
    -------
    bool
        Whether ``descendant`` is indeed a descendant of ``ancestor``.

    See also
    --------
    is_descendant_or_self : Get whether path is descendant of other path or is equivalent to it

    Examples
    --------
    >>> is_descendant(Path('a'), Path('a'))
    False
    >>> is_descendant(Path('a/b'), Path('a'))
    True
    >>> is_descendant(Path('a'), Path('a/b'))
    False
    >>> is_descendant(Path('a'), Path('a/..'))
    False
    '''
    return _is_descendant(descendant, ancestor, or_self=False)

def is_descendant_or_self(descendant, ancestor):
    '''
    Get whether path is descendant of other path or is equivalent to it.

    Uses the absolute path, so symlinks, ... do not affect this.

    Parameters
    ----------
    descendant : ~pathlib.Path
        Supposed descendant.
    ancestor : ~pathlib.Path
        Supposed ancestor.

    Returns
    -------
    bool
        Whether ``descendant`` is indeed a descendant of ``ancestor`` or they
        are equivalent (equal after path normalisation).

    See also
    --------
    is_descendant : Get whether path is descendant of other path

    Examples
    --------
    >>> is_descendant_or_self(Path('a'), Path('a'))
    True
    >>> is_descendant_or_self(Path('a/b'), Path('a'))
    True
    >>> is_descendant_or_self(Path('a'), Path('a/b'))
    False
    >>> is_descendant_or_self(Path('a'), Path('a/..'))
    False
    '''
    return _is_descendant(descendant, ancestor, or_self=True)

def _is_descendant(descendant, ancestor, or_self):
    ancestor = ancestor.resolve()
    descendant = descendant.resolve()
    return ancestor in descendant.parents or (or_self and ancestor == descendant)
