from pathlib import Path
here = Path(__file__).parent

import sys
sys.path.append(here / 'chicken_turtle')

from chicken_turtle.setuptools import setup

# setup
setup(
    # custom attrs
    here=here,
    readme_file='readme.md',
    
    # overridden
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    # Note: you must add ancestors of any applicable classifier too
    classifiers='''
        Natural Language :: English
        Intended Audience :: Developers
        Development Status :: 2 - Pre-Alpha
        Topic :: Software Development
        Topic :: Software Development :: Libraries
        Operating System :: POSIX
        Operating System :: POSIX :: AIX
        Operating System :: POSIX :: BSD
        Operating System :: POSIX :: BSD :: BSD/OS
        Operating System :: POSIX :: BSD :: FreeBSD
        Operating System :: POSIX :: BSD :: NetBSD
        Operating System :: POSIX :: BSD :: OpenBSD
        Operating System :: POSIX :: GNU Hurd
        Operating System :: POSIX :: HP-UX
        Operating System :: POSIX :: IRIX
        Operating System :: POSIX :: Linux
        Operating System :: POSIX :: Other
        Operating System :: POSIX :: SCO
        Operating System :: POSIX :: SunOS/Solaris
        Operating System :: Unix
        License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)
        Programming Language :: Python
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.2
        Programming Language :: Python :: 3.3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: 3.5
    ''',
    
    # standard
    name='chicken_turtle',
    description="Python 3 project template, tailored to the author's needs",
    author='Tim Diels',
    author_email='timdiels.m@gmail.com',

    url='https://github.com/timdiels/chicken_turtle', # project homepage
 
    license='LGPL3',
    
    # What does your project relate to?
    keywords='',
 
    # Required dependencies
    setup_requires=[],  # required to run setup.py. I'm not aware of any setup tool that uses this though
    install_requires='pytest click'.split(),
 
    # Optional dependencies
    extras_require={
        'dev': ['pypandoc'],
        'test': [],
    },
)