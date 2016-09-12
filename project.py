project = dict(
    name='chicken_turtle_util',
    package_name='chicken_turtle_util',
    human_friendly_name='Chicken Turtle Util',
    description="Python 3 utility library",
    author='Tim Diels',
    author_email='timdiels.m@gmail.com',
    python_version=(3,4),
    readme_file='README.rst',
    url='https://github.com/timdiels/chicken_turtle_util', # project homepage
    download_url='https://github.com/timdiels/chicken_turtle_util/releases/v{version}.tar.gz', # Template for url to download source archive from. You can refer to the current version with {version}. You can get one from github or gitlab for example.
    license='LGPL3',
 
    # What does your project relate to?
    keywords='development util library utility utilities',
    
    # Package indices to release to using `ct-release`
    # These names refer to those defined in ~/.pypirc.
    # For pypi, see http://peterdowns.com/posts/first-time-with-pypi.html
    # For devpi, see http://doc.devpi.net/latest/userman/devpi_misc.html#using-plain-setup-py-for-uploading
    index_test = 'pypitest',  # Index to use for testing a release, before releasing to `index_production`. `index_test` can be set to None if you have no test index
    index_production = 'pypi',
    
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    # Note: you must add ancestors of any applicable classifier too
    classifiers='''
        Natural Language :: English
        Intended Audience :: Developers
        Development Status :: 4 - Beta
        Topic :: Software Development
        Topic :: Software Development :: Libraries
        Operating System :: Android
        Operating System :: BeOS
        Operating System :: iOS
        Operating System :: MacOS
        Operating System :: MacOS :: MacOS 9
        Operating System :: MacOS :: MacOS X
        Operating System :: Microsoft
        Operating System :: Microsoft :: MS-DOS
        Operating System :: Microsoft :: Windows
        Operating System :: Microsoft :: Windows :: Windows 3.1 or Earlier
        Operating System :: Microsoft :: Windows :: Windows 7
        Operating System :: Microsoft :: Windows :: Windows 95/98/2000
        Operating System :: Microsoft :: Windows :: Windows CE
        Operating System :: Microsoft :: Windows :: Windows NT/2000
        Operating System :: Microsoft :: Windows :: Windows Server 2003
        Operating System :: Microsoft :: Windows :: Windows Server 2008
        Operating System :: Microsoft :: Windows :: Windows Vista
        Operating System :: Microsoft :: Windows :: Windows XP
        Operating System :: OS/2
        Operating System :: OS Independent
        Operating System :: Other OS
        Operating System :: PalmOS
        Operating System :: PDA Systems
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
        Programming Language :: Python :: 3 :: Only
        Programming Language :: Python :: 3.2
        Programming Language :: Python :: 3.3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: Implementation
        Programming Language :: Python :: Implementation :: CPython
        Programming Language :: Python :: Implementation :: Stackless
        Topic :: Utilities
        Topic :: Software Development
        Topic :: Software Development :: Libraries
        Topic :: Software Development :: Libraries :: Python Modules
    ''',
)
