"""
Setuptools based setup functions.

See:
- https://packaging.python.org/en/latest/distributing.html
- https://github.com/pypa/sampleproject
"""

# want to keep this as lean on required deps as possible

from setuptools import setup as setup_, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

def setup(**args):    
    # read some of args
    name = args['name']
    here = args['here']
    src_root = here
    
    try:
        import pypandoc
        args['long_description'] = pypandoc.convert(args['readme_file'], 'rst')
    except ImportError:
        args['long_description'] = open(args['readme_file']).read()
    del args['readme_file']
    
    args['classifiers'] = [line.strip() for line in args['classifiers'].splitlines() if line.strip()]
    
    # various tidbits
    pkg_root = src_root / name
    
    # version
    version_file = pkg_root / 'version.py'
    with version_file.open() as f:
        code = compile(f.read(), str(version_file), 'exec')
        locals = {}
        exec(code, None, locals)
        __version__ = locals['__version__']
        
    # data files
    data_files = [str(path - pkg_root) for path in (pkg_root / 'data').walk(filter=lambda x: not x.isdir())]
    
    # override
    relative_src_root = str(src_root - here)
    args.update(
        version=__version__,
        
        # List packages
        packages=find_packages(relative_src_root),
        package_dir={'': relative_src_root}, # tell setup where packages are
        
        # List data files
        package_data={name: data_files},
    )
    
    # setup
    setup_(**args)
