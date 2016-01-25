from chicken_turtle.setuptools import setup
from pathlib import Path

here = Path(__file__).parent

# setup
setup(
    # custom attrs
    here = here,
    readme_file='readme.md',
    
    # Overridden
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    # Note: you must add ancestors of any applicable classifier too
    classifiers='''
        Natural Language :: English
        Intended Audience :: Developers
        Environment :: TODO if any
        Development Status :: 2 - Pre-Alpha
        Topic :: TODO
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
    name='$project_name',
    description='Short description',
    author='your name',
    author_email='your_email@example.com',

    url='https://example.com/project/home', # project homepage
 
    license='LGPL3',
 
    # What does your project relate to?
    keywords='keyword1 key-word2',
 
    # Required dependencies
    setup_requires='pypandoc'.split(), # required to run setup.py. I'm not aware of any setup tool that uses this though
    install_requires=(
        'pypi-dep-1 pypydep2 '
        'moredeps '
    ).split(),
 
    # Optional dependencies
    extras_require={
        'dev': ''.split(),
        'test': 'pytest pytest-benchmark pytest-timeout pytest-xdist freezegun'.split(),
    },
 
    # Auto generate entry points
    entry_points={
        'console_scripts': [
            'mycli = project_name.main:main', # just an example, any module will do, this template doesn't care where you put it
        ],
    },
)