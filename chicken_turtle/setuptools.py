# Copyright (C) 2016 Tim Diels <timdiels.m@gmail.com>
# 
# This file is part of Chicken Turtle.
# 
# Chicken Turtle is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Chicken Turtle is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with Chicken Turtle.  If not, see <http://www.gnu.org/licenses/>.

"""
Setuptools based setup functions.

See:
- https://packaging.python.org/en/latest/distributing.html
- https://github.com/pypa/sampleproject
"""

# want to keep this as lean on required deps as possible

from setuptools import setup as setup_, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
import os

def setup(**args):    
    # read some of args
    name = args['name']
    here = args['here']
    del args['here']
    
    try:
        import pypandoc
        args['long_description'] = pypandoc.convert(args['readme_file'], 'rst')
    except ImportError:
        args['long_description'] = open(args['readme_file']).read()
    del args['readme_file']
    
    args['classifiers'] = [line.strip() for line in args['classifiers'].splitlines() if line.strip()]
    
    # various tidbits
    pkg_root = here / name
    
    # version
    version_file = pkg_root / 'version.py'
    with version_file.open() as f:
        code = compile(f.read(), str(version_file), 'exec')
        locals_ = {}
        exec(code, None, locals_)
        __version__ = locals_['__version__']
        
    # data files
    data_files = [str(parent / file) for parent, _, files in os.walk(str(pkg_root / 'data')) for file in files]
    
    # override
    args.update(
        version=__version__,
        
        # List packages
        packages=find_packages(name),
        
        # List data files
        package_data={name: data_files},
    )
    
    # setup
    setup_(**args)
